// Records the built-in camera until SIGINT or SIGTERM, then finalizes the movie.
// SIGHUP is ignored: closing the afk window must not end the recording.
// One-second fragments keep the file playable if the process is killed outright.

import AVFoundation
import CoreMedia
import Darwin
import Foundation

struct CaptureError: LocalizedError {
    let message: String
    var errorDescription: String? { message }
}

final class Recorder: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    private let session = AVCaptureSession()
    private let frames = DispatchQueue(label: "cam.frames")
    private let lock = NSLock()
    private var path = ""
    private var writer: AVAssetWriter?
    private var input: AVAssetWriterInput?
    private var recording = false
    private var finishing = false
    private var accepting = true
    private var announced = false
    private var limit: TimeInterval = 0

    func start(path: String) throws {
        self.path = path
        try authorize()
        guard let device = AVCaptureDevice.default(
            .builtInWideAngleCamera, for: .video, position: .unspecified
        ) ?? AVCaptureDevice.default(for: .video) else {
            throw CaptureError(message: "no camera")
        }
        let camera = try AVCaptureDeviceInput(device: device)
        let output = AVCaptureVideoDataOutput()
        output.videoSettings = [
            kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange)
        ]
        output.alwaysDiscardsLateVideoFrames = true
        output.setSampleBufferDelegate(self, queue: frames)
        session.beginConfiguration()
        guard session.canAddInput(camera), session.canAddOutput(output) else {
            throw CaptureError(message: "cannot use the camera")
        }
        session.addInput(camera)
        session.addOutput(output)
        session.commitConfiguration()
        configure(device)
        session.startRunning()
        guard session.isRunning else {
            throw CaptureError(message: "camera did not start")
        }
    }

    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection
    ) {
        guard accepting else { return }
        if writer == nil {
            do {
                try open(sampleBuffer)
            } catch {
                fputs("cam: \(error.localizedDescription)\n", stderr)
                exit(1)
            }
        }
        guard let input, input.isReadyForMoreMediaData else { return }
        if !input.append(sampleBuffer), let writer, writer.status == .failed {
            fputs("cam: \(writer.error?.localizedDescription ?? "could not write the movie")\n", stderr)
            exit(1)
        }
        guard !announced else { return }
        announced = true
        // Detach only after a frame is in the file. Doing it sooner leaves the
        // permission prompt with no terminal session, and the request never
        // returns. The afk window hangs up after the pointer exits.
        _ = setsid()
        if limit > 0 {
            DispatchQueue.global(qos: .utility).asyncAfter(deadline: .now() + limit) {
                self.stop()
            }
        }
        let token = "ready\n"
        _ = token.withCString { write(STDOUT_FILENO, $0, strlen($0)) }
    }

    func stop() {
        frames.async { self.finish() }
    }

    func record(for seconds: TimeInterval) {
        limit = seconds
    }

    private func open(_ sampleBuffer: CMSampleBuffer) throws {
        guard let format = CMSampleBufferGetFormatDescription(sampleBuffer) else {
            throw CaptureError(message: "camera did not start")
        }
        let dim = CMVideoFormatDescriptionGetDimensions(format)
        let writer = try AVAssetWriter(outputURL: URL(fileURLWithPath: path), fileType: .mov)
        writer.movieFragmentInterval = CMTime(seconds: 1, preferredTimescale: 1)
        let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: Int(dim.width),
            AVVideoHeightKey: Int(dim.height),
            AVVideoCompressionPropertiesKey: [
                AVVideoAverageBitRateKey: 1_200_000,
                AVVideoExpectedSourceFrameRateKey: 15,
                AVVideoMaxKeyFrameIntervalKey: 15,
                AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
            ],
        ])
        input.expectsMediaDataInRealTime = true
        guard writer.canAdd(input) else {
            throw CaptureError(message: "cannot write the movie")
        }
        writer.add(input)
        guard writer.startWriting() else {
            throw CaptureError(message: writer.error?.localizedDescription ?? "cannot write the movie")
        }
        writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sampleBuffer))
        self.writer = writer
        self.input = input
        lock.lock()
        recording = true
        lock.unlock()
    }

    private func finish() {
        lock.lock()
        if finishing {
            lock.unlock()
            return
        }
        finishing = true
        let recording = self.recording
        self.recording = false
        lock.unlock()
        guard recording, let writer, let input else {
            exit(0)
        }
        accepting = false
        input.markAsFinished()
        writer.finishWriting {
            if writer.status != .completed {
                let message = writer.error?.localizedDescription ?? "could not finish the movie"
                fputs("cam: \(message)\n", stderr)
                exit(1)
            }
            exit(0)
        }
    }

    private func configure(_ device: AVCaptureDevice) {
        guard (try? device.lockForConfiguration()) != nil else { return }
        defer { device.unlockForConfiguration() }
        let frame = CMTime(value: 1, timescale: 15)
        let ranges = device.activeFormat.videoSupportedFrameRateRanges
        if ranges.contains(where: { $0.minFrameRate <= 15 && $0.maxFrameRate >= 15 }) {
            device.activeVideoMinFrameDuration = frame
            device.activeVideoMaxFrameDuration = frame
        }
    }

    private func authorize() throws {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            return
        case .notDetermined:
            var granted = false
            var answered = false
            AVCaptureDevice.requestAccess(for: .video) { allowed in
                granted = allowed
                answered = true
                CFRunLoopStop(CFRunLoopGetMain())
            }
            let deadline = Date().addingTimeInterval(60)
            while !answered && Date() < deadline {
                CFRunLoopRunInMode(.defaultMode, 0.2, false)
            }
            if !granted {
                throw CaptureError(message: "camera access denied")
            }
        default:
            throw CaptureError(message: "camera access denied")
        }
    }
}

setvbuf(stdout, nil, _IONBF, 0)
signal(SIGPIPE, SIG_IGN)
signal(SIGHUP, SIG_IGN)
signal(SIGINT, SIG_IGN)
signal(SIGTERM, SIG_IGN)

guard CommandLine.arguments.count == 2 || CommandLine.arguments.count == 3 else {
    fputs("cam: recording path expected\n", stderr)
    exit(2)
}

let recorder = Recorder()
if CommandLine.arguments.count == 3 {
    guard let seconds = TimeInterval(CommandLine.arguments[2]), seconds > 0 else {
        fputs("cam: duration expected\n", stderr)
        exit(2)
    }
    recorder.record(for: seconds)
}
let signals = DispatchQueue(label: "cam.signals")
let interrupt = DispatchSource.makeSignalSource(signal: SIGINT, queue: signals)
let terminate = DispatchSource.makeSignalSource(signal: SIGTERM, queue: signals)
interrupt.setEventHandler { recorder.stop() }
terminate.setEventHandler { recorder.stop() }
interrupt.resume()
terminate.resume()

do {
    try recorder.start(path: CommandLine.arguments[1])
} catch {
    fputs("cam: \(error.localizedDescription)\n", stderr)
    exit(1)
}

dispatchMain()
