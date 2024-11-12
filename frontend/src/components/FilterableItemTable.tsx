import { ItemsQuery, SearchParams } from "../types";
import ItemTable from "./ItemTable";
import SearchBar from "./SearchBar";

interface FilterableItemTableProps {
  categories: string[];
  itemsQuery: ItemsQuery | null;
  isFetchingItems: boolean;
  isFetchingCategories: boolean;
  onSearch: (searchParams: SearchParams) => void;
}

const FilterableItemTable: React.FC<FilterableItemTableProps> = ({
  categories,
  itemsQuery,
  isFetchingItems,
  isFetchingCategories,
  onSearch,
}) => {

  return (
    <div>
      <SearchBar
        categories={categories}
        isFetchingCategories={isFetchingCategories}
        isFetchingItems={isFetchingItems}
        onSearch={onSearch}
      />
      <ItemTable
        itemsQuery={itemsQuery}
        isFetchingItems={isFetchingItems}
      />
    </div>
  );
}

export default FilterableItemTable;