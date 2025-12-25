import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { notFound } from "next/navigation";
import { MDXRemote } from "next-mdx-remote/rsc";
import FAQAccordion from "@/components/FAQAccordion";

const BLOG_PATH = path.join(process.cwd(), "content/blog");

type Props = {
  params: { slug: string };
};

export async function generateStaticParams() {
  const files = fs.readdirSync(BLOG_PATH);

  return files.map((file) => ({
    slug: file.replace(/\.mdx$/, ""),
  }));
}

const mdxComponents = {
  FAQ: FAQAccordion,
};

export default async function BlogPost({ params }: Props) {
  const filePath = path.join(BLOG_PATH, `${params.slug}.mdx`);

  if (!fs.existsSync(filePath)) {
    notFound();
  }

  const file = fs.readFileSync(filePath, "utf8");
  const { content, data } = matter(file);

  return (
    <article className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-[40px] font-extrabold leading-tight tracking-tighter mb-6">
        {data.title}
      </h1>

      <p className="text-gray-500 mt-2">{data.date}</p>

      <div className="prose mt-6 post-style">
        {await MDXRemote({
          source: content,
          components: mdxComponents,
        })}
      </div>
    </article>
  );
}
