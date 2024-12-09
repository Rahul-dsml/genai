import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { QueryClientProvider, QueryClient } from "react-query";
import ContextProvider from './components/Context/GeminiContext.jsx'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')).render(
 
    <QueryClientProvider client={queryClient}>
    <ContextProvider>
    <App />
    </ContextProvider>
    </QueryClientProvider>
    
  
)
