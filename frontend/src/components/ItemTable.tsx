import { ItemsQuery } from "../types";
import ItemRow from "./ItemRow";

interface ItemTableProps {
  itemsQuery: ItemsQuery | null;
  isFetchingItems: boolean;
}

const ItemTable: React.FC<ItemTableProps> = ({
  itemsQuery,
  isFetchingItems
}) => {
  const totalPrice = itemsQuery?.totalPrice;
  const rows: React.ReactNode[] = [];
  const items = itemsQuery?.items;
  if (items) {
    items.forEach((item) => {
      rows.push(
        <ItemRow
          key={item.id}
          item={item}
        />
      );
    });
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Category</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>{rows.length === 0 ? 'No items to display' : rows}</tbody>
      <tfoot>{totalPrice ? `Total price: ${totalPrice}` : ''}</tfoot>
    </table>
  );
}

export default ItemTable;