import { Item } from "../types";
import { capitalise } from "../utils";

interface ItemRowProps {
  item: Item
}

const ItemRow: React.FC<ItemRowProps> = ({ item }) => {
  return (
    <tr>
      <td>{item.name}</td>
      <td>{capitalise(item.category)}</td>
      <td>{item.price}</td>
    </tr>
  )
}

export default ItemRow;