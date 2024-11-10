import { Product } from "../types";
import ProductTable from "./ProductTable";
import SearchBar from "./SearchBar";

interface FilterableProductTable {
  products: Product[]
}

const FilterableProductTable: React.FC<FilterableProductTable> = ({ products }) => {
  return (
    <div>
      <SearchBar />
      <ProductTable products={products} />
    </div>
  );
}

export default FilterableProductTable;