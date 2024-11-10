const SearchBar: React.FC = () => {
  return (
    <div className="search-bar">
      <input type="text" placeholder="Search for a product" />
      <button>Search</button>
    </div>
  );
};

export default SearchBar;