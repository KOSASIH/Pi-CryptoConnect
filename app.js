import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { CryptoDataProvider } from './contexts/CryptoDataContext';
import { CryptoListPage } from './pages/CryptoListPage';
import { CryptoDetailPage } from './pages/CryptoDetailPage';
import { AppConfig } from './config/app.config';
import { CryptoConnectModel } from './models/CryptoConnectModel';
import { getCryptoData } from './utils/crypto';

const App: React.FC = () => {
  const [cryptos, setCryptos] = useState<CryptoConnectModel[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getCryptoData();
      setCryptos(data);
    };

    fetchData();
  }, []);

  return (
    <CryptoDataProvider value={cryptos}>
      <Router>
        <Switch>
          <Route path="/" exact component={CryptoListPage} />
          <Route path="/crypto/:id" component={CryptoDetailPage} />
        </Switch>
      </Router>
    </CryptoDataProvider>
  );
};

export default App;
