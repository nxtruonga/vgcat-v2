import './globals.css' // https://nextjs.org/docs/app/guides/tailwind-v3-css
import React from 'react';
import { AntdRegistry } from '@ant-design/nextjs-registry';

const RootLayout = ({ children }: React.PropsWithChildren) => (
  <html
    lang="en"
    style={{ height: 'calc(100% - 0px)' }}
  >
    <body
      style={{ height: 'inherit' }}
    >
      <AntdRegistry>{children}</AntdRegistry>
    </body>
  </html>
);

export default RootLayout;