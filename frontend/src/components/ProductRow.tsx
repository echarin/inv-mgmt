import { Product } from "../types";

interface ProductRowProps {
  product: Product
}

const ProductRow: React.FC<ProductRowProps> = ({ product }) => {
  const name = product.stocked ?
    product.name :
    <span style={{ color: 'red' }}>
      {product.name}
    </span>;

  return (
    <tr>
      <td>{name}</td>
      <td>{product.price}</td>
    </tr>
  );
}

export default ProductRow;