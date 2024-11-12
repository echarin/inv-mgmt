import { Button, FormControl, FormHelperText, InputLabel, MenuItem, Select } from "@mui/material";
import { DateOrTimeView, DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { Dayjs } from "dayjs";
import { useState } from "react";
import { SearchParams } from "../types";
import { capitalise } from "../utils";

interface SearchBarProps {
  categories: string[];
  isFetchingCategories: boolean;
  isFetchingItems: boolean;
  onSearch: (searchParams: SearchParams) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  categories,
  isFetchingCategories,
  isFetchingItems,
  onSearch,
}) => {
  const [dtFrom, setDtFrom] = useState<Dayjs | null>(null);
  const [dtTo, setDtTo] = useState<Dayjs | null>(null);
  const [category, setCategory] = useState<string>('');

  const [categoryError, setCategoryError] = useState<string>('');
  const [dateError, setDateError] = useState<string>('');

  const datePickerViews: DateOrTimeView[] = [
    'year', 'month', 'day', 'hours', 'minutes', 'seconds'
  ];

  const isDataValid = () => {
    let valid = true;
    setCategoryError('');
    setDateError('');

    if (category && !categories.includes(category)) {
      setCategoryError(`Category ${category} does not exist.`);
      valid = false;
    }

    if (dtFrom && dtTo && dtTo.isBefore(dtFrom)) {
      setDateError('End date must be after start date.');
      valid = false;
    }

    return valid;
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!isDataValid()) {
      return;
    }

    // Format dates to required string format
    const dateFormat = "YYYY-MM-DD HH:mm:ss";
    const formattedDtFrom = dtFrom ? dtFrom.format(dateFormat) : '';
    const formattedDtTo = dtTo ? dtTo.format(dateFormat) : '';

    const searchParams: SearchParams = {
      dt_from: formattedDtFrom,
      dt_to: formattedDtTo,
      category: category.trim()
    }

    onSearch(searchParams);
  };

  const handleClearFields = () => {
    setDtFrom(null);
    setDtTo(null);
    setCategory('');
    setCategoryError('');
    setDateError('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <DateTimePicker
            label="Start date"
            views={datePickerViews}
            value={dtFrom}
            onChange={(d) => setDtFrom(d)}
            slotProps={{
              textField: {
                error: false // Don't display error in start date
              },
              field: {
                clearable: true
              }
            }}
          />
          <DateTimePicker
            label="End date"
            views={datePickerViews}
            value={dtTo}
            onChange={(d) => setDtTo(d)}
            slotProps={{
              textField: {
                error: Boolean(dateError),
                helperText: dateError
              },
              field: {
                clearable: true
              }
            }}
          />
          <FormControl
            error={Boolean(categoryError)}
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
              <MenuItem value="">
                <em>All Categories</em>
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
            type="submit"
            disabled={isFetchingCategories || isFetchingItems}
          >
            {isFetchingItems ? 'Searching...' : 'Search'}
          </Button>
        </div>
      </LocalizationProvider>
    </form>
  );
};

export default SearchBar;