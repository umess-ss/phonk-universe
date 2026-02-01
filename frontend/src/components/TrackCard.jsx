const TrackCard = ({track, isSelected, onSelect, formatDuration}) => (
    <div 
        className={`track-card ${isSelected ? 'selected' : ''}`}
        onClick={() => onSelect(track)}
    >
        <div className="track-cover">
            {/* UPDATED: Using track.thumbnail from your MongoDB model */}
            {track.thumbnail ? (
                <img src={track.thumbnail} alt={track.title} />
            ) : (
                <div className="cover-placeholder">🎧</div>
            )}
        </div>

        <div className="track-info">
            <h3 className="track-title">{track.title}</h3>
            <p className="track-artist">{track.artist}</p>
            
            <div className="track-meta">
                <span className="track-genre">{track.genre}</span>
                
                {/* NOTE: If your MongoDB doesn't have duration yet, 
                    this will show as 0:00 or NaN. */}
                {track.duration && (
                    <span className="track-duration">{formatDuration(track.duration)}</span>
                )}
                
                {/* Shows platform (youtube/spotify) since you have that in your DB */}
                <span className="track-platform">{track.platform}</span>
            </div>
        </div>
        <button className="play-btn">▶️</button>
    </div>
)

export default TrackCard;