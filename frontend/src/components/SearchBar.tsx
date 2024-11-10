interface SearchBarProps {
  filterText: string;
  inStockOnly: boolean;
  onFilterTextChange: (filterText: string) => void;
  onInStockOnlyChange: (inStockOnly: boolean) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  filterText, 
  inStockOnly,
  onFilterTextChange,
  onInStockOnlyChange
}) => {
  return (
    <form>
      <input 
        type="text" 
        value={filterText}
        placeholder="Search..."
        onChange={(e) => onFilterTextChange(e.target.value)} />
      <label>
        <input 
          type="checkbox" 
          checked={inStockOnly}
          onChange={(e) => onInStockOnlyChange(e.target.checked)} />
        {' '}
        Only show products in stock
      </label>
    </form>
  );
}

export default SearchBar;