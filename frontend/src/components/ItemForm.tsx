import { useState } from "react";
import { ItemCreate, SearchParams } from "../types";
import { capitalise, PRICE_REGEX } from "../utils";

import { routes } from "../config";
import apiClient from "../services/axios";

interface ItemFormProps {
  categories: string[];
  isFetchingCategories: boolean;
  onItemCreated: (searchParams: SearchParams) => void;
  searchParams: SearchParams;
}

const ItemForm: React.FC<ItemFormProps> = ({
  categories,
  isFetchingCategories,
  onItemCreated,
  searchParams
}) => {
  const [name, setName] = useState<string>('');
  // store form input values as strings, even for numbers
  const [price, setPrice] = useState<string>('');
  const [category, setCategory] = useState<string>('');

  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const [successMsg, setSuccessMsg] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string>('');

  const isDataValid = (): string | null => {
    if (!name.trim() || !category.trim() || !price.trim()) {
      return 'Please fill in all fields.';
    }

    const priceRegex = PRICE_REGEX;
    if (!priceRegex.test(price) || parseFloat(price) < 0) {
      return 'Price must be a non-negative number with up to two decimal places.';
    }

    return null;
  };

  const resetForm = () => {
    setName('');
    setPrice('');
    setCategory('');
    setErrorMsg('');
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const validationError = isDataValid();
    if (validationError) {
      setErrorMsg(validationError);
      return;
    }

    const itemData: ItemCreate = {
      name: name.trim(),
      category: category.trim(),
      price: parseFloat(price)
    }

    try {
      setSuccessMsg('');
      setIsSubmitting(true);

      const response = await apiClient.post(routes.create_item, itemData);

      resetForm();

      setSuccessMsg(`Item created successfully with id ${response.data.id}.`);

      onItemCreated(searchParams);
    } catch (error) {
      console.error(`Error creating item: ${error}.`);
      setErrorMsg('Error creating item. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {isFetchingCategories ? (
        <div>Loading categories...</div>
      ) : (
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
              min="0"
              placeholder="5.50"
              onChange={(e) => setPrice(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Category:</label>
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
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
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Submitting...' : "Save Item"}
            </button>
          </div>
          {errorMsg && <div className="error">{errorMsg}</div>}
          {!errorMsg && successMsg && <div className="success">{successMsg}</div>}
        </form>
      )}
    </>
  );
};

export default ItemForm;