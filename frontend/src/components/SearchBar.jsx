const SearchBar = ({searchQuery, setSearchQuery, onSearch, onClear}) => (
    <div className="search-container">
        <form onSubmit={onSearch} className="search-form">
            <input 
                type="text"
                placeholder="Search tracks or artists...."
                value={searchQuery}
                onChange={(e)=> setSearchQuery(e.target.value)}
                className="search-input"
                />
            <button type="submit" className="search-btn">
                Search
            </button>
            {searchQuery && 
            (<button type="button" onClick={onClear} className="clear-btn">Clear</button>)
            }
        </form>
    </div>
)

export default SearchBar;