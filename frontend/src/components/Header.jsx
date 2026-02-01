const Header = ({activeTab, setActiveTab}) =>(
  <header className="header">
    <div className="header-content">
      <h1 className="logo">PHONK UNIVERSE</h1>
      <nav className="nav">
        {['tracks', 'playlists', 'about'].map((tab)=>(
          <button 
          key={tab}
          className={activeTab === tab ? 'nav-btn active' : 'nav-btn'}
          onClick={()=> setActiveTab(tab)}>
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </nav>
    </div>
  </header>
)

export default Header;