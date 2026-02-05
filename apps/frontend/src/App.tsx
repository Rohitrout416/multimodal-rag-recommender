import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';
import VirtualMirror from './pages/VirtualMirror';
import Trends from './pages/Trends';
import { Button } from '@/components/ui/button';
import { LogOut, Shirt, Sparkles, MessageSquare } from 'lucide-react';

function NavBar() {
    const location = useLocation();
    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    };

    if (['/login', '/register'].includes(location.pathname)) return null;

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center max-w-screen-2xl">
                <div className="mr-4 flex">
                    <a className="mr-6 flex items-center space-x-2 font-bold" href="/">
                        <span>FashNet</span>
                    </a>
                    <div className="flex gap-4">
                        <Link to="/"><Button variant="ghost" className="text-sm font-medium transition-colors hover:text-primary"><MessageSquare className="mr-2 h-4 w-4" /> Chat</Button></Link>
                        <Link to="/virtual-mirror"><Button variant="ghost" className="text-sm font-medium transition-colors hover:text-primary"><Shirt className="mr-2 h-4 w-4" /> Try-On</Button></Link>
                        <Link to="/trends"><Button variant="ghost" className="text-sm font-medium transition-colors hover:text-primary"><Sparkles className="mr-2 h-4 w-4" /> Trends</Button></Link>
                    </div>
                </div>
                <div className="ml-auto flex items-center space-x-2">
                    <Button variant="outline" size="sm" onClick={handleLogout}>
                        <LogOut className="mr-2 h-4 w-4" /> Logout
                    </Button>
                </div>
            </div>
        </nav>
    );
}

function App() {
    // Simple auth check
    const isAuthenticated = !!localStorage.getItem('token');

    return (
        <Router>
            <div className="min-h-screen bg-background font-sans antialiased">
                <NavBar />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route
                        path="/"
                        element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/virtual-mirror"
                        element={isAuthenticated ? <VirtualMirror /> : <Navigate to="/login" />}
                    />
                    <Route
                        path="/trends"
                        element={isAuthenticated ? <Trends /> : <Navigate to="/login" />}
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
