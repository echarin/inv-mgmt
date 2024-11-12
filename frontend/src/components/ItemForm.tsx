import { Button, FormControl, FormHelperText, InputAdornment, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import { useState } from "react";
import { routes } from "../config";
import apiClient from "../services/axios";
import { ItemCreate, SearchParams } from "../types";
import { capitalise, PRICE_REGEX } from "../utils";

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

  const [nameError, setNameError] = useState<string>('');
  const [priceError, setPriceError] = useState<string>('');
  const [categoryError, setCategoryError] = useState<string>('');
  const [successMsg, setSuccessMsg] = useState<string>('');

  const isDataValid = () => {
    let valid = true;
    setNameError('');
    setPriceError('');
    setCategoryError('');

    if (!name.trim()) {
      setNameError('Name is required.');
      valid = false;
    }

    if (!price.trim()) {
      setPriceError('Price is required.');
      valid = false;
    } else {
      const priceRegex = PRICE_REGEX;
      if (!priceRegex.test(price) || parseFloat(price) < 0) {
        setPriceError('Price must be a non-negative number with up to two decimal places.');
        valid = false;
      }
    }

    if (!category.trim()) {
      setCategoryError('Category is required.');
      valid = false;
    } else if (!categories.includes(category.trim())) {
      setCategoryError('Invalid category selected.');
      valid = false;
    }

    return valid;
  };

  const resetForm = () => {
    setName('');
    setPrice('');
    setCategory('');
    setNameError('');
    setPriceError('');
    setCategoryError('');
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!isDataValid()) {
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
      setSuccessMsg('');
      setNameError('Error creating item. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (<>
    {isFetchingCategories ? (
      <div>Loading categories...</div>
    ) : (
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <TextField
            id="name"
            label="Name"
            type="text"
            value={name}
            placeholder="Pencil"
            onChange={(e) => setName(e.target.value)}
            error={Boolean(nameError)}
            helperText={nameError}
            required
          />
          <TextField
            id="price"
            label="Price"
            type="number"
            value={price}
            placeholder="5.50"
            onChange={(e) => setPrice(e.target.value)}
            error={Boolean(priceError)}
            helperText={priceError}
            required
            slotProps={{
              input: {
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
                inputProps: {
                  step: 0.01,
                  min: 0,
                },
              }
            }}
          />
          <FormControl
            error={Boolean(categoryError)}
            required
            style={{ minWidth: 200 }}
          >
            <InputLabel id="category-label">Category</InputLabel>
            <Select
              labelId="category-label"
              id="category"
              value={category}
              label="Category"
              onChange={(e) => setCategory(e.target.value)}
            >
              <MenuItem value="" disabled>
                Select category
              </MenuItem>
              {categories.map((c) => (
                <MenuItem key={c} value={c}>
                  {capitalise(c)}
                </MenuItem>
              ))}
            </Select>
            {categoryError && <FormHelperText>{categoryError}</FormHelperText>}
          </FormControl>
          <Button
            variant="contained"
            type="submit"
            disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : "Save Item"}
          </Button>
        </div>
        {successMsg && (
          <Typography variant="body1" color="success">
            {successMsg}
          </Typography>
        )}
      </form>
    )}
  </>);
};

export default ItemForm;