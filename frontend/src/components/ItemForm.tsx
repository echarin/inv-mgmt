import { useState } from "react";
import { CATEGORIES } from "../mockData";
import { Category, ItemCreate } from "../types";
import { capitalise, PRICE_REGEX } from "../utils";
import axios from "axios";

const ItemForm: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [price, setPrice] = useState<number>(0);
  const [category, setCategory] = useState<Category | ''>('');
  const [errorMsg, setErrorMsg] = useState<string>('');

  const hasError = errorMsg !== '';
  const categories = CATEGORIES;

  const isDataValid = ({ 
    name, 
    price, 
    category 
  }: { 
    name: string, 
    price: number, 
    category: Category 
  }) => {
    if (!name.trim() || !category || !price) {
      setErrorMsg('Please fill in all fields');
      return false;
    }

    const priceRegex = PRICE_REGEX;
    const priceStr = price.toString();
    if (!priceRegex.test(priceStr) || parseFloat(priceStr) <= 0) {
      setErrorMsg('Price must be a positive number with up to two decimal places');
      return false;
    }

    setErrorMsg('');
    return true;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    console.log("Submitted");
    event.preventDefault();

    if (category === '') return;
    if (!isDataValid({ name, price, category })) return;

    const itemData: ItemCreate = {
      name: name.trim(),
      category: category as Category,
      price: parseFloat(price.toString())
    }

    try {
      const response = await axios.post(
        'test-url',
        itemData,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      setName('');
      setCategory('');
      setPrice(0);
      setErrorMsg('');
    } catch (error) {
      console.error(`Error creating item: ${error}`);
      setErrorMsg('Error creating item. Please try again later.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input
          id="name"
          type="text"
          value={name}
          placeholder="Pencil"
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Price:</label>
        <input
          id="price"
          type="number"
          value={price}
          step="0.01"
          min="0.01"
          placeholder="5.5"
          onChange={(e) => setPrice(parseFloat(e.target.value))}
          required
        />
      </div>
      <div>
        <label>Category:</label>
        <select
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value as Category)}
          required
        >
          <option value="" disabled>Select category</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {capitalise(category)}
            </option>
          ))}
        </select>
      </div>
      <div>
        <button type="submit">Save Item</button>
      </div>
      {hasError && <div className="error">{errorMsg}</div>}
    </form>
  );
};

export default ItemForm;