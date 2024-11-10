import { ItemsQuery } from "../types";
import ItemRow from "./ItemRow";

interface ItemTableProps {
  itemsQuery: ItemsQuery;
}

const ItemTable: React.FC<ItemTableProps> = ({ itemsQuery }) => {
  const rows: React.ReactNode[] = [];
  const items = itemsQuery.items;
  items.forEach((item) => {
    rows.push(
      <ItemRow
        key={item.id}
        item={item}
      />
    );
  });

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
      <tfoot>Total price: ${itemsQuery.totalPrice}</tfoot>
    </table>
  );
}

export default ItemTable;