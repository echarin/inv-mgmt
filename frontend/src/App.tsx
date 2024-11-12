import { CssBaseline } from '@mui/material';
import AppLayout from './components/AppLayout';
import InventoryManagementSystem from './components/InventoryManagementSystem';

export default function App() {
  return (
    <AppLayout>
      <CssBaseline>
        <InventoryManagementSystem />
      </CssBaseline>
    </AppLayout>
  );
}