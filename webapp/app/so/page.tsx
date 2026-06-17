import Image from 'next/image'

export default function Page() {
  return (
    <div className='m-8'>
      <div>SO</div>
      <Image src="/file.svg" alt="File" width={100} height={100} />
    </div>
  )
}