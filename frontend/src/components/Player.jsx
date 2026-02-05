import { useState, useRef, useEffect } from 'react';

const Player = ({ track, formatDuration, onClose }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [loading, setLoading] = useState(true);
    const [audioUrl, setAudioUrl] = useState(null);
    const [error, setError] = useState(null);
    const audioRef = useRef(null);

    const API_URL = 'http://localhost:8000';

    // Fetch the playable audio URL from backend
    useEffect(() => {
        const fetchAudioUrl = async () => {
            if (track.platform === 'youtube') {
                try {
                    setLoading(true);
                    setError(null);
                    
                    const response = await fetch(`${API_URL}/proxy/youtube/${track.externalID}`);
                    
                    if (!response.ok) {
                        throw new Error('Failed to fetch audio URL');
                    }
                    
                    const data = await response.json();
                    setAudioUrl(data.url);
                    
                } catch (err) {
                    console.error('Error fetching audio:', err);
                    setError('Failed to load audio. Please try another track.');
                    setLoading(false);
                }
            } else {
                setError('Only YouTube tracks are supported currently');
                setLoading(false);
            }
        };

        fetchAudioUrl();
    }, [track]);

    // Initialize audio when URL is ready
    useEffect(() => {
        if (!audioRef.current || !audioUrl) return;

        const audio = audioRef.current;

        // Reset state
        setIsPlaying(false);
        setCurrentTime(0);

        // Load the new track
        audio.load();

        // Event listeners
        const handleLoadedMetadata = () => {
            setDuration(audio.duration);
            setLoading(false);
        };

        const handleTimeUpdate = () => {
            setCurrentTime(audio.currentTime);
        };

        const handleEnded = () => {
            setIsPlaying(false);
            setCurrentTime(0);
        };

        const handleError = (e) => {
            console.error('Audio error:', e);
            setLoading(false);
            setError('Playback failed. The audio stream may have expired.');
        };

        const handleCanPlay = () => {
            setLoading(false);
        };

        audio.addEventListener('loadedmetadata', handleLoadedMetadata);
        audio.addEventListener('timeupdate', handleTimeUpdate);
        audio.addEventListener('ended', handleEnded);
        audio.addEventListener('error', handleError);
        audio.addEventListener('canplay', handleCanPlay);

        return () => {
            audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
            audio.removeEventListener('timeupdate', handleTimeUpdate);
            audio.removeEventListener('ended', handleEnded);
            audio.removeEventListener('error', handleError);
            audio.removeEventListener('canplay', handleCanPlay);
        };
    }, [audioUrl]);

    // Play/Pause handler
    const togglePlayPause = () => {
        if (!audioRef.current || !audioUrl) return;

        if (isPlaying) {
            audioRef.current.pause();
            setIsPlaying(false);
        } else {
            audioRef.current.play()
                .then(() => setIsPlaying(true))
                .catch(err => {
                    console.error('Playback error:', err);
                    setError('Playback failed. Try refreshing.');
                });
        }
    };

    // Seek handler
    const handleSeek = (e) => {
        if (!audioRef.current || !audioUrl) return;
        const progressBar = e.currentTarget;
        const clickX = e.nativeEvent.offsetX;
        const width = progressBar.offsetWidth;
        const seekTime = (clickX / width) * duration;
        audioRef.current.currentTime = seekTime;
        setCurrentTime(seekTime);
    };

    // Skip forward/backward
    const skipTime = (seconds) => {
        if (!audioRef.current || !audioUrl) return;
        audioRef.current.currentTime = Math.max(0, Math.min(duration, currentTime + seconds));
    };

    const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;

    return (
        <div className="player">
            {/* Audio element */}
            {audioUrl && (
                <audio
                    ref={audioRef}
                    src={audioUrl}
                    preload="metadata"
                />
            )}

            <div className="player-content">
                <div className="player-track-info">
                    <strong>{track.title}</strong> - {track.artist}
                    {loading && <span className="loading-indicator"> ⏳ Loading...</span>}
                    {error && <span className="error-indicator"> ⚠️ {error}</span>}
                </div>

                <div className="player-controls">
                    <button 
                        className="control-btn" 
                        onClick={() => skipTime(-10)}
                        disabled={loading || error}
                        title="Skip back 10s"
                    >
                        ⏮️
                    </button>
                    
                    <button 
                        className="control-btn play-pause" 
                        onClick={togglePlayPause}
                        disabled={loading || error}
                        title={isPlaying ? 'Pause' : 'Play'}
                    >
                        {loading ? '⏳' : (isPlaying ? '⏸️' : '▶️')}
                    </button>
                    
                    <button 
                        className="control-btn" 
                        onClick={() => skipTime(10)}
                        disabled={loading || error}
                        title="Skip forward 10s"
                    >
                        ⏭️
                    </button>
                </div>

                <div className="player-time">
                    <span>{formatDuration(Math.floor(currentTime))}</span>
                    <div 
                        className="progress-bar" 
                        onClick={handleSeek}
                        style={{ cursor: loading || error ? 'not-allowed' : 'pointer' }}
                    >
                        <div 
                            className="progress" 
                            style={{ width: `${progressPercent}%` }}
                        />
                    </div>
                    <span>{formatDuration(Math.floor(duration || track.duration || 0))}</span>
                </div>

                <button className="close-player" onClick={onClose} title="Close player">✕</button>
            </div>
        </div>
    );
};

export default Player;