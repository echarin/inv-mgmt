import { CATEGORIES } from "../mockData";
import { capitalise } from "../utils";

const ItemForm: React.FC = () => {
  const categories = CATEGORIES;

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input type="text" placeholder="Pencil" />
      </div>
      <div>
        <label>Price:</label>
        <input type="text" placeholder="5.5" />
      </div>
      <div>
        <label>Category:</label>
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
        <button type="submit">Save item</button>
      </div>
    </form>
  );
};

export default ItemForm;