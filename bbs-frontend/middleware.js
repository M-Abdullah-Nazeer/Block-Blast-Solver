// middleware.js (root directory)
export function middleware(request) {
    const url = request.nextUrl;
    if (url.protocol === 'http:') {
      return Response.redirect(`https://${url.hostname}${url.pathname}`, 301);
    }
  }