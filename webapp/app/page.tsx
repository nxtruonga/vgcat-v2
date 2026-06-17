'use client'

import React, { useState } from 'react';
import {
  SettingOutlined,
  WechatWorkOutlined,
  LineChartOutlined,
  AudioOutlined,
  ArrowUpOutlined,
  LoadingOutlined,
  MenuOutlined,
} from '@ant-design/icons';
import { Button, Layout, Menu, theme, Input, Grid } from 'antd';
import axios from "axios";
import type { AxiosInstance } from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from 'rehype-highlight'

const { useBreakpoint } = Grid;
const { Header, Sider, Content } = Layout;
const { TextArea } = Input;
const API_PATH = "/so.v1.SoService/GetIfm"
// const GnBaseURL = "http://localhost:8000" + API_PATH;
const GnBaseURL = "https://endpoint-fe23e4b9-3cd1-4d93-b8f8-60535c5ec142.agentbase-runtime.aiplatform.vngcloud.vn" + API_PATH;
const gnApi: AxiosInstance = axios.create({
  // baseURL: GnBaseURL,
  timeout: 30000,
  headers: { "X-Custom-Header": "todo" },
});

const App: React.FC = () => {
  const [value, setValue] = useState('');
  const [collapsed, setCollapsed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [modelResp, setModelResp] = useState("");
  const { token: { colorBgContainer } } = theme.useToken();
  const screens = useBreakpoint();

  const onClickSearchAI = async () => {
    await searchAIGreenNode(value, setIsLoading, setModelResp);
  }
  const onPressEnterSearchAI = async () => {
    await searchAIGreenNode(value, setIsLoading, setModelResp);
  }

  return (
    <Layout
      style={{
        height: 'inherit'
      }}
    >
      <Sider
        style={{
          background: colorBgContainer,
          borderRight: '1px solid lightgray'
        }}
        breakpoint="md"
        onBreakpoint={(broken) => {
          console.log('-- onBreakpoint', broken);
          setCollapsed(broken)
        }}

        trigger={null}
        collapsible
        collapsed={collapsed}
        collapsedWidth="50"
      >
        <div style={{
          height: '50px',
        }}
        >
        </div>
        <Menu
          style={{ borderInlineEnd: 'none' }}
          theme="light"
          mode="inline"
          defaultSelectedKeys={['1']}
          items={[
            { key: '1', icon: <WechatWorkOutlined />, label: 'Chat' },
            { key: '2', icon: <LineChartOutlined />, label: 'SO' },
            { key: '3', icon: <SettingOutlined />, label: 'Settings' },
          ]}
        />
      </Sider>
      <Layout
        style={{ background: colorBgContainer }}
      >
        <Header
          style={{
            display: 'flex',
            alignItems: 'center',
            height: '50px',
            padding: '0px',
            background: colorBgContainer,
            // borderBottom: '1px solid green'
          }}
        >
          <Button
            type="text"
            icon={<MenuOutlined />}
            onClick={() => setCollapsed(!collapsed)}
          />
        </Header>
        <Content
          className='p-4 pt-8'
        >
          <div style={{
            display: 'flex',
            position: 'relative'
          }}>
            <TextArea
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onPressEnter={onPressEnterSearchAI}
              placeholder="Ask AI"
              autoSize={{ minRows: 3, maxRows: 8 }}
            />
            <div className='mr-6 mb-2'
              style={{
                display: 'flex',
                position: 'absolute',
                right: '0',
                bottom: '0'
              }}>
              <Button type="text" shape="circle" size={'large'} icon={<AudioOutlined />} />
              <Button type="primary" shape="circle" size={'large'} icon={<ArrowUpOutlined />}
                onClick={onClickSearchAI}
              />
            </div>
          </div>
          <div
            className='my-2'
            style={{ visibility: isLoading ? "visible" : "hidden" }}
          >
            <LoadingOutlined />
          </div>
          <div
            style={{ fontSize: 'initial' }}
          >
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
            >
              {modelResp}
            </ReactMarkdown>
          </div>
        </Content>
      </Layout>
    </Layout >
  );
};
export default App;

async function searchAIGreenNode(value: string,
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>,
  setModelResp: React.Dispatch<React.SetStateAction<string>>) {
  const msg_1: GnReqMessage = createGnReqMessage("", "");
  const msg_2: GnReqMessage = createGnReqMessage("user", value);
  const payload: GreenNodePayload = { messages: [msg_1, msg_2] };
  try {
    setIsLoading(true);
    const response = await gnApi.post(GnBaseURL, payload);
    setIsLoading(false);
    const text = response?.data?.messages[0]?.text ?? "Hệ thống đang có lỗi. Vui lòng thử lại sau.";
    setModelResp(text);
  } catch (error) {
    setIsLoading(false);
    setModelResp(String(error));
  }
}

//--
function createGnReqMessage(role: string, content: string): GnReqMessage {
  return {
    role: role,
    content: content,
  };
}
interface GnReqMessage {
  role: string;
  content: string;
};
interface GreenNodePayload {
  messages: GnReqMessage[];
};
interface GnModelResponse {
  id: string;
  role: string;
  type: string;
  model: string;
  messages: GnMsgItem[];
};
interface GnMsgItem {
  type: string;
  text: string;
};