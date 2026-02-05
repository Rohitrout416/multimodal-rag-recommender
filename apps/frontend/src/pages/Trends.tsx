import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge'; // Note: standard Shadcn badge might not be set up, so we'll use standard div if fails or we need to create it. Assuming basic div for now or we can implement Badge.

interface Trend {
    keyword: string;
    score: number;
    change: string;
    image_url: string;
    description: string;
}

export default function Trends() {
    const [trends, setTrends] = useState<Trend[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTrends = async () => {
            try {
                const response = await api.get('/trends');
                setTrends(response.data);
            } catch (error) {
                console.error('Failed to fetch trends:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchTrends();
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-6xl">
            <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
                <span className="text-3xl">📈</span> Global Fashion Trends
            </h1>

            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <Card key={i} className="animate-pulse">
                            <div className="h-48 bg-muted rounded-t-lg"></div>
                            <CardContent className="p-4 space-y-2">
                                <div className="h-6 bg-muted rounded w-3/4"></div>
                                <div className="h-4 bg-muted rounded w-1/2"></div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {trends.map((trend, idx) => (
                        <Card key={idx} className="overflow-hidden hover:shadow-lg transition-shadow group cursor-pointer">
                            <div className="relative h-48 overflow-hidden">
                                <img
                                    src={trend.image_url}
                                    alt={trend.keyword}
                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                />
                                <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-xs font-bold">
                                    Score: {trend.score}
                                </div>
                            </div>
                            <CardHeader className="p-4 pb-2">
                                <div className="flex justify-between items-start">
                                    <CardTitle className="text-xl">{trend.keyword}</CardTitle>
                                    <span className={`text-sm font-medium ${trend.change.startsWith('+') ? 'text-green-600' : 'text-red-500'}`}>
                                        {trend.change}
                                    </span>
                                </div>
                            </CardHeader>
                            <CardContent className="p-4 pt-0">
                                <p className="text-sm text-muted-foreground">
                                    {trend.description}
                                </p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    );
}
