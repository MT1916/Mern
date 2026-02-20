import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { EditRentalPage } from './pages/EditRentalPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/rental/:id/edit" element={<EditRentalPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
