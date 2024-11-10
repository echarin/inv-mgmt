import { ITEMS_QUERY } from "../mockData";
import { jsonToCamelCase } from "../utils";
import FilterableItemTable from "./FilterableItemTable";
import ItemForm from "./ItemForm";

const InvMgmtSystem: React.FC = () => {
  const items_query = jsonToCamelCase(ITEMS_QUERY);

  return (
    <div>
      <h1>Inventory Management System</h1>
      <ItemForm />
      <FilterableItemTable itemsQuery={items_query} />
    </div>
  )
}

export default InvMgmtSystem;