import fs from "fs";
import path from "path";
import matter from "gray-matter";
import Link from "next/link";
import Image from "next/image";
import FAQAccordion from "@/components/FAQAccordion";

const BLOG_PATH = path.join(process.cwd(), "content/blog");

export default function BlogArchive() {
  const files = fs.readdirSync(BLOG_PATH);

  const posts = files.map(file => {
    const filePath = path.join(BLOG_PATH, file);
    const content = fs.readFileSync(filePath, "utf8");
    const { data } = matter(content);

    return {
      slug: file.replace(/\.mdx$/, ""),
      title: data.title,
      description: data.description,
      image: data.image
    };
  });



  return (
    <main className="max-w-screen-2xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-8 text-center">Blogs</h1>

      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map(post => (
          <li key={post.slug}>
            <Link href={`/blog/${post.slug}`}>
              {post.image && (
                <Image
                  src={post.image}
                  alt={post.title}
                  width={400}
                  height={225}
                  className="rounded-lg w-full"
                />
              )}

              <h2 className="text-lg font-semibold mt-4">
                {post.title}
              </h2>
              <p className="text-gray-600 mt-2">{post.description}</p>
            </Link>
          </li>
        ))}
      </ul>

      {/* Client Component */}
      
    </main>
  );
}
