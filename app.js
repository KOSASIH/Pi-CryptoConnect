import React, { useEffect, useState, Suspense, lazy } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { CryptoDataProvider } from './contexts/CryptoDataContext';
import { AppConfig } from './config/app.config';
import { CryptoConnectModel } from './models/CryptoConnectModel';
import { getCryptoData } from './utils/crypto';
import { Spinner } from './components/Spinner'; // A simple loading spinner component

// Lazy load the pages
const CryptoListPage = lazy(() => import('./pages/CryptoListPage'));
const CryptoDetailPage = lazy(() => import('./pages/CryptoDetailPage'));

const App: React.FC = () => {
  const [cryptos, setCryptos] = useState<CryptoConnectModel[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getCryptoData();
        setCryptos(data);
      } catch (err) {
        setError('Failed to fetch cryptocurrency data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Spinner />; // Show loading spinner while fetching data
  }

  if (error) {
    return <div>Error: {error}</div>; // Display error message
  }

  return (
    <CryptoDataProvider value={cryptos}>
      <Router>
        <Suspense fallback={<Spinner />}>
          <Switch>
            <Route path="/" exact component={CryptoListPage} />
            <Route path="/crypto/:id" component={CryptoDetailPage} />
          </Switch>
        </Suspense>
      </Router>
    </CryptoDataProvider>
  );
};

export default App;
