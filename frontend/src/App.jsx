import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import TrackCard from "./components/TrackCard";
import Player from "./components/Player";
import "./App.css";


const API_URL = 'http://localhost:8000';





function App(){
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('tracks');
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedTrack, setSelectedTrack] = useState(null);


    useEffect(()=> {fetchTracks();},[]);



    const fetchTracks = async () => {
  try {
    setLoading(true);
    const response = await fetch(`${API_URL}/tracks`);
    if (!response.ok) throw new Error('Failed to fetch tracks');
    
    const result = await response.json();
    setTracks(result.data || []); 
    
    setError(null);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};




    const handleSearch = async (e) => {
      e.preventDefault();
      if (!searchQuery.trim()) return fetchTracks;
try {
    setLoading(true);
    const response = await fetch(`${API_URL}/tracks/search/${encodeURIComponent(searchQuery)}`);
    if (!response.ok) throw new Error('Search failed');
    
    const result = await response.json();
    setTracks(result.data || []); 
    setError(null);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
    };


    const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };


  return (
    <div className="app">
      <Header activeTab={activeTab} setActiveTab={setActiveTab}/>
      <SearchBar 
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onSearch={handleSearch}
        onClear={()=> {setSearchQuery(''); fetchTracks();}}
      />

      <main className="main-content">
        {error && <div className="error-message">⚠️ {error} <button onClick={fetchTracks}>Retry</button></div>}

        {activeTab === 'tracks' && (
          <section className="tracks-section">
            <h2 className="section-title">All Tracks</h2>
            {loading ? <p>Loading...</p> :(
              <div className="tracks-grid">
                {tracks.map(track=> (
                  <TrackCard 
                    key={track._id}
                    track={track}
                    isSelected={selectedTrack?.id === track._id}
                    onSelect={setSelectedTrack}
                    formatDuration={formatDuration}
                  />
                ))}
              </div>
            )}
          </section>
        )}


        {activeTab === 'playlists' && <div className="coming-soon">Playlists Coming Soon</div>}
        {activeTab === 'about' && <div className="about-content">Phonk Universe v1.0</div>}
      </main>
      

      {selectedTrack && (
        <Player 
          track={selectedTrack} 
          formatDuration={formatDuration} 
          onClose={() => setSelectedTrack(null)} 
        />
      )}
    </div>
  );
}

export default App;