import { useState } from "react";
import { SearchParams } from "../types";
import { capitalise } from "../utils";

interface SearchBarProps {
  categories: string[];
  isFetchingCategories: boolean;
  onSearch: (searchParams: SearchParams) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  categories,
  isFetchingCategories,
  onSearch,
}) => {
  const [dtFrom, setDtFrom] = useState<string>('');
  const [dtTo, setDtTo] = useState<string>('');
  const [category, setCategory] = useState<string>('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    // todo: validation

    const searchParams: SearchParams = {
      dt_from: dtFrom.trim(),
      dt_to: dtTo.trim(),
      category: category.trim()
    }

    onSearch(searchParams);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          id="dateFrom"
          type="text"
          value={dtFrom}
          placeholder="Search by start date"
          onChange={(e) => setDtFrom(e.target.value)}
        />
        <input
          id="dateTo"
          type="text"
          value={dtTo}
          placeholder="Search by end date"
          onChange={(e) => setDtTo(e.target.value)}
        />
      </div>
      <div>
        <label>Filter by category:</label>
        {isFetchingCategories && <div>Loading categories...</div>}
        <select
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {capitalise(category)}
            </option>
          ))}
        </select>
      </div>
      <div>
        <button type="submit">
          Search
        </button>
      </div>
    </form>
  );
};

export default SearchBar;