import { CATEGORIES } from "../mockData";
import { capitalise } from "../utils";

const SearchBar: React.FC = () => {
  const categories = CATEGORIES;
  
  const handleSubmit = (event: React.FormEvent) => {
    // do something
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input type="text" placeholder="Search by start date" />
        <input type="text" placeholder="Search by end date" />
      </div>
      <div>
        <label>Filter by category:</label>
        <select>
          <option value="" disabled>Select category</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {capitalise(category)}
            </option>
          ))}
        </select>
      </div>
      <div>
        <button type="submit">Search</button>
      </div>
    </form>
  );
};

export default SearchBar;