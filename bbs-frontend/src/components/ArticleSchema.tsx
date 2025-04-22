// components/ArticleSchema.tsx (SERVER COMPONENT)
export const ArticleSchema = () => {
    // Article Schema
    const articleSchema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Your Article Title",
        "description": "Brief summary of the article",
        "image": "https://yourdomain.com/article-image.webp",
        "author": {
            "@type": "Person",
            "name": "Author Name"
        },
        "datePublished": "2024-01-01",
        "publisher": {
            "@type": "Organization",
            "name": "Your Tool",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yourdomain.com/logo.webp"
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