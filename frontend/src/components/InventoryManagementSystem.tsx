import { useCallback, useEffect, useState } from "react";
import { routes } from "../config";
import apiClient from "../services/axios";
import { ItemsQuery, SearchParams } from "../types";
import { jsonToCamelCase } from "../utils";
import FilterableItemTable from "./FilterableItemTable";
import ItemForm from "./ItemForm";

const InventoryManagementSystem: React.FC = () => {
  const [itemsQuery, setItemsQuery] = useState<ItemsQuery | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [currentSearchParams, setCurrentSearchParams] = useState<SearchParams>({
    dt_from: '',
    dt_to: '',
    category: ''
  });

  const [isFetchingItems, setIsFetchingItems] = useState<boolean>(false);
  const [isFetchingCategories, setIsFetchingCategories] = useState<boolean>(false);

  const [errorMsg, setErrorMsg] = useState<string>('');

  // Populate category dropdowns
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setIsFetchingCategories(true);
        const response = await apiClient.get(routes.read_categories);
        setCategories(response.data);
      } catch (error) {
        console.error(`Error fetching categories: ${error}.`);
        setErrorMsg("Error fetching categories. Please try again later.");
      } finally {
        setIsFetchingCategories(false);
      }
    };

    fetchCategories();
  }, []);

  // Fetch items based on search params
  const fetchItemsWithParams = useCallback(async (searchParams: SearchParams) => {
    try {
      setIsFetchingItems(true);
      setCurrentSearchParams(searchParams);
      const response = await apiClient.post(routes.read_items, searchParams);
      setItemsQuery(jsonToCamelCase(response.data) as ItemsQuery);
    } catch (error) {
      console.error(`Error fetching items: ${error}.`);
      setErrorMsg("Error fetching items. Please try again later.");
    } finally {
      setIsFetchingItems(false);
    }
  }, []);

  return (
    <div>
      <h1>Inventory Management System</h1>
      {errorMsg && <div className="error">{errorMsg}</div>}
      <ItemForm
        categories={categories}
        isFetchingCategories={isFetchingCategories}
        onItemCreated={fetchItemsWithParams}
        searchParams={currentSearchParams}
      />
      <FilterableItemTable
        categories={categories}
        itemsQuery={itemsQuery}
        isFetchingItems={isFetchingItems}
        isFetchingCategories={isFetchingCategories}
        onSearch={fetchItemsWithParams}
      />
    </div>
  )
}

export default InventoryManagementSystem;