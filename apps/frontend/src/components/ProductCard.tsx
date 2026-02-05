import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { ExternalLink } from "lucide-react";

interface Product {
    id: number;
    name: string;
    description: string;
    category: string;
    price: float;
    image_url: string;
}

interface ProductCardProps {
    product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
    return (
        <Card className="w-[200px] flex-shrink-0 text-sm overflow-hidden flex flex-col">
            <div className="h-[150px] w-full overflow-hidden bg-white">
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-contain hover:scale-105 transition-transform"
                />
            </div>
            <CardHeader className="p-3 pb-0">
                <CardTitle className="text-base truncate" title={product.name}>
                    {product.name}
                </CardTitle>
                <p className="text-xs text-muted-foreground font-medium">${product.price}</p>
            </CardHeader>
            <CardContent className="p-3 py-2 flex-grow">
                <p className="text-xs text-muted-foreground line-clamp-2">
                    {product.description}
                </p>
            </CardContent>
            <CardFooter className="p-3 pt-0">
                <Button size="sm" variant="outline" className="w-full text-xs h-7">
                    View Details <ExternalLink className="ml-1 h-3 w-3" />
                </Button>
            </CardFooter>
        </Card>
    );
}
