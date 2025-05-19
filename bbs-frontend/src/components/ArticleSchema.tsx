// components/ArticleSchema.tsx (SERVER COMPONENT)
export const ArticleSchema = () => {
    // Article Schema
    const articleSchema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Block Blast Solver",
        "description": "Explains the steps to use block blast solver, elaborates the AI features of the game helper.",
        "image": "https://blockblastsolverai.com/article-image.webp",
        "author": {
            "@type": "Person",
            "name": "Abdullah"
        },
        "datePublished": "2025-05-18",
        "publisher": {
            "@type": "Organization",
            "name": "Block Blast Solver",
            "logo": {
                "@type": "ImageObject",
                "url": "https://blockblastsolverai.com/block-blast-solver-logo.webp"
            }
        }
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
        />
    );
};