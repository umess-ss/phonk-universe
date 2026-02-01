const Player = ({track, formatDuration, onclose}) => (
    <div className="player">
        <div className="player-content">
            <div className="player-track-info">
                <strong>{track.title}</strong> - {track.artist}
            </div>
            <div className="player-controls">
                <button className="control-btn">⏮️</button>
                <button className="control-btn play-pause">▶️</button>
                <button className="control-btn">⏭️</button>
            </div>
            <div className="player-time">
                <span>0:00</span>
                <div className="progress-bar">
                    <div className="progress" style={{ width: '0%' }}></div>
                </div>
                <span>{formatDuration(track.duration)}</span>
            </div>
            <button className="close-player" onClick={onClose}>✕</button>
        </div>
    </div>
)

export default Player;