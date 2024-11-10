import { Item, ItemsQuery } from "../types";
import ItemTable from "./ItemTable";
import SearchBar from "./SearchBar";

interface FilterableItemTableProps {
  itemsQuery: ItemsQuery
}

const FilterableItemTable: React.FC<FilterableItemTableProps> = ({ itemsQuery }) => {
  return (
    <div>
      <h1>FilterableItemTable</h1>
      <SearchBar />
      <ItemTable itemsQuery={itemsQuery} />
    </div>
  );
}

export default FilterableItemTable;