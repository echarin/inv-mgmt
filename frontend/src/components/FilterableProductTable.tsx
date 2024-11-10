import { useState } from "react";
import { Product } from "../types";
import ProductTable from "./ProductTable";
import SearchBar from "./SearchBar";

interface FilterableProductTable {
  products: Product[]
}

const FilterableProductTable: React.FC<FilterableProductTable> = ({ products }) => {
  const [filterText, setFilterText] = useState<string>('');
  const [inStockOnly, setInStockOnly] = useState<boolean>(false);

  return (
    <div>
      <SearchBar
        filterText={filterText}
        inStockOnly={inStockOnly}
        onFilterTextChange={setFilterText}
        onInStockOnlyChange={setInStockOnly} />
      <ProductTable 
        products={products} 
        filterText={filterText}
        inStockOnly={inStockOnly} />
    </div>
  );
}

export default FilterableProductTable;