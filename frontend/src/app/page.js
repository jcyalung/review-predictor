"use client";
import Image from "next/image";
import { useRouter } from "next/navigation";
import Header from './header.js';
const push = useRouter();
export default function Root() {
  push('/home');
}
