import './App.css';
import FilterableProductTable from './components/FilterableProductTable';
import { PRODUCTS } from './mockData';

export default function App() {
  return <FilterableProductTable products={PRODUCTS} />;
}