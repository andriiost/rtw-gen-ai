import React from 'react'
import Instagram from '../assets/socials/instagram.png'
import X from '../assets/socials/x.png'
import Youtube from '../assets/socials/youtube.png'
import Linkedin from '../assets/socials/linkedin.png'
import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="w-full border-t-2 border-slate-300">
      <section className="grid grid-cols-3 p-16 pl-64 pr-40">
        <div className="flex flex-col items-start gap-3 text-sm font-bold leading-6">
          <p>Day of Mourning</p>
          <p>Health and safety statistics</p>
          <p>Open Data</p>
          <p>Accessibility</p>
          <p>Privacy</p>
          <p>Fair Practices Commission</p>
        </div>
        <div className="flex flex-col items-start gap-3 text-sm font-bold leading-6">
          <p>Contact Us</p>
          <p>Land Acknowledgement</p>
          <p>Health and Safety Index</p>
          <p>Careers</p>
          <p>Terms of use</p>
          <p>Other languages</p>
        </div>
        <div className="text-sm font-normal leading-6 text-footerGray">
          <p>Fatal or catastrophic workplace accidents</p>
          <p className='pb-8'>Call us 1-800-387-0750</p>
          
          <p>Contact us</p>
          <p>1-800-387-0750</p>
          <div className='flex pt-8 space-x-8'>
              <img src={Linkedin}/>
              <img src={X}/>
              <img src={Youtube}/>
              <img src={Instagram}/>
          </div>
        </div>
      </section>
      <section className="bg-footer">
        <p className="text-slate-100 p-8 text-center">© 2024, Workplace Safety and Insurance Board</p>
      </section>
    </footer>
  )
}
