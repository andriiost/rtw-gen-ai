import React from "react";
import { useParams } from "react-router-dom";
import Select from "react-select";
import { useState } from "react";
import { Link } from "react-router-dom";
import { Dialog, DialogBackdrop, DialogPanel } from "@headlessui/react";
import { useEffect } from "react";
import Loading from "../../components/Loading";
import Error from "../../components/Error";
import { useNavigate } from "react-router-dom";
export default function VerificationPage() {
  const { id } = useParams();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  // fetching and such here
  const [title, setTitle] = useState("");
  const [area, setArea] = useState("");
  const [nature, setNature] = useState("");
  const [industry, setIndustry] = useState("");
  const [accommodation, setAccommodation] = useState("");
  const [link, setLink] = useState("");
  const currentDate = new Date().toISOString().slice(0, 10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePreview = () => {
    setOpen(true);
  };

  const handleSubmit =  async (e) => {
    e.preventDefault();
    const data = {
      accommodation_name: title,
      accommodation_descriptions: accommodation,
      verified : true,
      data_created : currentDate,
      //the following are not in the table...
      injury_location: area,
      injury_nature: nature,
      industry: industry,
    }
    try { 
      setLoading(true)
      setError(null)
      //req

      setLoading(true)
    } catch (err) {
      setError('An error occurred and the accommodation may not be verified/changed!')
      setLoading(false)
    }
    //switch page? or have a success page
    navigate('/verifications')
  };

  const  handleDelete = async () => {
    try{
      setError(null)
      const res = await fetch(`http://127.0.0.1:5000/delete_accommodation/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })
      const data = await res.json();
      console.log(data);
      setError(null)
      navigate('/verifications')
    } catch (err) {
      setError('An error occurred and the accommodation may not be deleted!')
    }
  };

  useEffect(() => {
    const fetchAccommodation = async () => {
      try {
        setLoading(true)
        setError(null)
        let res = await fetch(`http://127.0.0.1:5000/accommodations/${id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        })
         res = await res.json();
         const data = res.data
        if (data.verified) {
          setError('Accommmodation has already been verified!');
          setTitle("");
          setArea("");
          setNature("");
          setIndustry("");
          setAccommodation("");
          setLink("");
          setLoading(false);
        } else {
        setTitle(data.accommodation_name);
        //should be an array do one for now
        setArea(data.injury_locations[0].injury_location_name);
        setNature(data.injury_natures[0].injury_nature_name);
        setIndustry(data.industries[0].industry_name);

        setAccommodation(data.accommodation_description);
        setLink(data.document.url);
        setError(null);
        setLoading(false);
        }
      } catch (err) {
        setError('An error occurred!')
        setTitle("");
        setArea("");
        setNature("");
        setIndustry("");
        setAccommodation("");
        setLink("");
        setLoading(false);
      }
    };
    fetchAccommodation();
  }, [id]);

  return (
    <div>
      {loading ? (
        <Loading />
      ) : (
        <div>
          {error ? (
            <Error
              title="Something Went Wrong"
              message={error}
              buttonLink="/verifications"
              buttonText="Back to Verfifications"
            />
          ) : (
            <div className="w-4/5 mx-auto">
              <div className="flex flex-row justify-between my-10">
                <div className="flex flex-row">
                  <Link to='/verifications' className="my-auto">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g id="angle-left-solid">
                        <path
                          id="Vector"
                          d="M14.2734 3.21094L6.02344 11.4609L5.50781 12L6.02344 12.5391L14.2734 20.7891L15.3516 19.7109L7.64062 12L15.3516 4.28906L14.2734 3.21094Z"
                          fill="black"
                        />
                      </g>
                    </svg>
                  </Link>

                  <div className="mx-10 text-4xl">{title}</div>
                </div>

                <div onClick={handleDelete} className="flex cursor-pointer flex-row">
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <g id="trash-alt">
                      <path
                        id="Vector"
                        d="M11.25 3C10.8574 3 10.4561 3.1377 10.1719 3.42188C9.8877 3.70605 9.75 4.10742 9.75 4.5V5.25H5.25V6.75H6V18.75C6 19.9834 7.0166 21 8.25 21H17.25C18.4834 21 19.5 19.9834 19.5 18.75V6.75H20.25V5.25H15.75V4.5C15.75 4.10742 15.6123 3.70605 15.3281 3.42188C15.0439 3.1377 14.6426 3 14.25 3H11.25ZM11.25 4.5H14.25V5.25H11.25V4.5ZM7.5 6.75H18V18.75C18 19.166 17.666 19.5 17.25 19.5H8.25C7.83398 19.5 7.5 19.166 7.5 18.75V6.75ZM9 9V17.25H10.5V9H9ZM12 9V17.25H13.5V9H12ZM15 9V17.25H16.5V9H15Z"
                        fill="#D90000"
                      />
                    </g>
                  </svg>
                  <p className="text-base ms-3 text-red-600">
                    Delete Accommodation
                  </p>
                </div>
              </div>

              <div className="flex">
                <div className="w-1/2 flex flex-col">
                  <form onSubmit={handleSubmit} className="flex flex-col">
                    <div className="flex flex-row text-base text-gray-900 my-4">
                      The following content was generated with AI, please
                      carefully verify its accuracy.{" "}
                    </div>

                    <label className="flex flex-col my-2">
                      <div className="flex flex-row text-base text-black">
                        Title <p className="text-red-600 ms-1">*</p>
                      </div>
                      <input
                        type="text"
                        onChange={(e) => {
                          setTitle(e.target.value);
                        }}
                        value={title}
                        className="border-2 p-2 rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 mt-2"
                      />
                    </label>

                    <label className="flex flex-col my-2">
                      <div className="flex flex-row text-base text-black">
                        Area of Body / Injury
                      </div>
                      <Select
                        options={[
                          { value: "Body systems", label: "Body systems" },
                          {
                            value: "Multiple body parts",
                            label: "Multiple body parts",
                          },
                          {
                            value: "Cranial region, including skull",
                            label: "Cranial region, including skull",
                          },
                          { value: "Leg(s)", label: "Leg(s)" },
                          {
                            value:
                              "Lower back (lumbar, sacral, coccygeal regions)",
                            label:
                              "Lower back (lumbar, sacral, coccygeal regions)",
                          },
                          { value: "Shoulder", label: "Shoulder" },
                          { value: "Ankle(s)", label: "Ankle(s)" },
                          {
                            value: "Finger(s), fingernail(s)",
                            label: "Finger(s), fingernail(s)",
                          },
                          { value: "Arm(s)", label: "Arm(s)" },
                          { value: "Wrist(s)", label: "Wrist(s)" },
                          { value: "Not Coded", label: "Not Coded" },
                          {
                            value: "Foot (feet), except toe(s)",
                            label: "Foot (feet), except toe(s)",
                          },
                          {
                            value: "Chest, including ribs, internal organs",
                            label: "Chest, including ribs, internal organs",
                          },
                          { value: "Pelvic region", label: "Pelvic region" },
                          {
                            value: "Upper extremities, unspecified, NEC",
                            label: "Upper extremities, unspecified, NEC",
                          },
                          {
                            value: "Multiple trunk locations",
                            label: "Multiple trunk locations",
                          },
                          {
                            value: "Multiple lower extremities locations",
                            label: "Multiple lower extremities locations",
                          },
                          {
                            value: "Hand(s), except finger(s)",
                            label: "Hand(s), except finger(s)",
                          },
                          {
                            value: "Upper back (cervical, thoracic regions)",
                            label: "Upper back (cervical, thoracic regions)",
                          },
                          {
                            value: "Multiple back regions",
                            label: "Multiple back regions",
                          },
                          { value: "Abdomen", label: "Abdomen" },
                          {
                            value: "Back, unspecified, NEC",
                            label: "Back, unspecified, NEC",
                          },
                          {
                            value: "Head, unspecified, NEC",
                            label: "Head, unspecified, NEC",
                          },
                          { value: "Eye(s)", label: "Eye(s)" },
                          { value: "Face", label: "Face" },
                          {
                            value: "Toe(s), toenail(s)",
                            label: "Toe(s), toenail(s)",
                          },
                          { value: "Ear(s)", label: "Ear(s)" },
                          {
                            value: "Multiple head locations",
                            label: "Multiple head locations",
                          },
                          {
                            value: "Lower extremities, unspecified, NEC",
                            label: "Lower extremities, unspecified, NEC",
                          },
                          {
                            value: "Trunk, unspecified, NEC",
                            label: "Trunk, unspecified, NEC",
                          },
                          {
                            value:
                              "Other body parts including unclassified, NEC",
                            label:
                              "Other body parts including unclassified, NEC",
                          },
                          { value: "Multiple", label: "Multiple" },
                          { value: "Other", label: "Other" },
                        ]}
                        defaultInputValue={area}
                        className="mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400"
                        onChange={(e) => setArea(e.value)}
                      />
                    </label>

                    <label className="flex flex-col my-2">
                      <div className="flex flex-row text-base text-black">
                        Nature of Injury
                      </div>
                      <Select
                        options={[
                          {
                            value: "Sprains and strains",
                            label: "Sprains and strains",
                          },
                          { value: "Psychiatric", label: "Psychiatric" },
                          { value: "Fractures", label: "Fractures" },
                          { value: "Concussion", label: "Concussion" },
                          {
                            value:
                              "Traumatic injuries, disorders, complications, unspecified, NEC",
                            label: "Bodysystems",
                          },
                          {
                            value: "Multiple traumatic injuries",
                            label: "Multiple traumatic injuries",
                          },
                          {
                            value: "Bruises, contusions",
                            label: "Bruises, contusions",
                          },
                          {
                            value: "COVID-19 novel coronavirus",
                            label: "COVID-19 novel coronavirus",
                          },
                          {
                            value:
                              "Intracranial injuries excluding concussions",
                            label:
                              "Intracranial injuries excluding concussions",
                          },
                          { value: "Other", label: "Other" },
                          { value: "Multiple", label: "Multiple" },
                        ]}
                        defaultInputValue={nature}
                        className="mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 "
                        onChange={(e) => {
                          setNature(e.value);
                        }}
                      />
                    </label>

                    <label className="flex flex-col my-2">
                      <div className="flex flex-row text-base text-black">
                        {" "}
                        NAICS Industry
                      </div>
                      <Select
                        options={[
                          {
                            value: "Agriculture, Forestry, Fishing and Hunting",
                            label: "Agriculture, Forestry, Fishing and Hunting",
                          },
                          {
                            value:
                              "Mining, Quarrying, and Oil and Gas Extraction",
                            label:
                              "Mining, Quarrying, and Oil and Gas Extraction",
                          },
                          { value: "Utilities", label: "Utilities" },
                          { value: "Construction", label: "Construction" },
                          { value: "Manufacturing", label: "Manufacturing" },
                          {
                            value: "Wholesale Trade",
                            label: "Wholesale Trade",
                          },
                          { value: "Retail Trade", label: "Retail Trade" },
                          {
                            value: "Transportation and Warehousing",
                            label: "Transportation and Warehousing",
                          },
                          { value: "Information", label: "Information" },
                          {
                            value: "Finance and Insurance",
                            label: "Finance and Insurance",
                          },
                          {
                            value: "Real Estate and Rental and Leasing",
                            label: "Real Estate and Rental and Leasing",
                          },
                          {
                            value:
                              "Professional, Scientific, and Technical Services",
                            label:
                              "Professional, Scientific, and Technical Services",
                          },
                          {
                            value: "Management of Companies and Enterprises",
                            label: "Management of Companies and Enterprises",
                          },
                          {
                            value:
                              "Administrative and Support and Waste Management",
                            label:
                              "Administrative and Support and Waste Management",
                          },
                          {
                            value: "Educational Services",
                            label: "Educational Services",
                          },
                          {
                            value: "Health Care and Social Assistance",
                            label: "Health Care and Social Assistance",
                          },
                          {
                            value: "Arts, Entertainment, and Recreation",
                            label: "Arts, Entertainment, and Recreation",
                          },
                          {
                            value: "Accommodation and Food Services",
                            label: "Accommodation and Food Services",
                          },
                          {
                            value:
                              "Other Services (except Public Administration)",
                            label:
                              "Other Services (except Public Administration)",
                          },
                          {
                            value: "Public Administration",
                            label: "Public Administration",
                          },
                          { value: "Multiple", label: "Multiple" },
                        ]}
                        defaultInputValue={industry}
                        className="mb-3 mt-2 border rounded-md border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400"
                        onChange={(e) => {
                          setIndustry(e.value);
                        }}
                      />
                    </label>

                    <label className="flex flex-col my-2">
                      <div className="flex flex-row justify-between text-base text-black">
                        <div className="flex flex-row">
                          Description of Accommodation{" "}
                          <p className="text-red-600 ms-1">*</p>
                        </div>
                        <div className="text-gray-400">500 words max</div>
                      </div>
                      <textarea
                        onChange={(e) => {
                          setAccommodation(e.target.value);
                        }}
                        value={accommodation}
                        required
                        type="input fied"
                        className="border-2 p-2 border-neutral-400 focus:ring-0  focus:outline-none focus:border-neutral-400 mt-2"
                      />
                    </label>
                  </form>
                  <div className="flex my-10 flex-row">
                    <button
                      onClick={handleSubmit}
                      className="flex w-2/4 mt-5 justify-center hover:bg-gray-800 rounded-3xl bg-sky-600 text-white px-3 py-3 me-1 text-sm font-semibold leading-6 shadow-sm
            "
                    >
                      Confirm Verification
                    </button>
                    <button
                      onClick={handlePreview}
                      className="flex w-1/3 mt-5 justify-center hover:border-gray-800 hover:text-white hover:bg-gray-800 rounded-3xl border-2 text-sky-600 border-sky-600 mx-1 px-3 py-3 text-sm font-semibold leading-6 shadow-sm"
                    >
                      Preview Page
                    </button>
                  </div>
                </div>

                <div className=" ms-10 w-1/2 flex flex-col">
                  <div>
                    <iframe
                      src="https://rtwblobwsib.blob.core.windows.net/rtwblobs/Accommodations - Construction - Bricklayer (WSIB Newsletter) (1)"
                      width="100%"
                      height="500px"
                      title="Original PDF"
                    ></iframe>
                  </div>
                  <div className="justify-end flex">
                    <Link to={link} className="text-sky-600 flex">
                      {" "}
                      <p className="underline mx-1 ">
                        {" "}
                        Open document in new window{" "}
                      </p>
                      <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g id="external-link-alt-solid">
                          <path
                            id="Vector"
                            d="M13.5 3.75V5.25H17.6719L8.46094 14.4609L9.53906 15.5391L18.75 6.32812V10.5H20.25V3.75H13.5ZM3.75 6.75V20.25H17.25V10.5L15.75 12V18.75H5.25V8.25H12L13.5 6.75H3.75Z"
                            fill="#0076BF"
                          />
                        </g>
                      </svg>
                    </Link>
                  </div>
                </div>
              </div>
              <Dialog open={open} onClose={setOpen} className="relative z-10">
                <DialogBackdrop
                  transition
                  className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in"
                />

                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                  <div className="flex min-h-full w-screen items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <DialogPanel
                      transition
                      className="relative transform w-full overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all data-[closed]:translate-y-4 data-[closed]:opacity-0 data-[enter]:duration-300 data-[leave]:duration-200 data-[enter]:ease-out data-[leave]:ease-in sm:my-8 sm:w-full sm:max-w-5xl data-[closed]:sm:translate-y-0 data-[closed]:sm:scale-95"
                    >
                      <div className="bg-gray-50 flex flex-row justify-between px-4 py-3 sm:px-6">
                        <div className="p-10 w-full flex flex-row justify-between ">
                          <div>
                            <p className="text-2xl">
                              Preview Accommodation Page
                            </p>
                            <p className="text-gray-500">
                              This is how the current information would appear
                              on the accommodation page.
                            </p>
                          </div>
                          <button
                            type="button"
                            data-autofocus
                            onClick={() => setOpen(false)}
                          >
                            <svg
                              width="24"
                              height="24"
                              viewBox="0 0 24 24"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <g id="close">
                                <path
                                  id="icon"
                                  d="M6.4 19L5 17.6L10.6 12L5 6.4L6.4 5L12 10.6L17.6 5L19 6.4L13.4 12L19 17.6L17.6 19L12 13.4L6.4 19Z"
                                  fill="#1D1B20"
                                />
                              </g>
                            </svg>
                          </button>
                        </div>
                      </div>
                      <div className="bg-white px-4 py-3">
                        {/* code here */}
                        <div className="">
                          <button
                          onClick = {() => setOpen(false)}
                          className="flex flex-row px-3 py-1 ms-10 rounded-3xl my-8 border-cyan-950 border">
                            <div className="my-auto">
                              <svg
                                width="16"
                                height="16"
                                viewBox="0 0 16 16"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                              >
                                <g id="angle-left-solid">
                                  <path
                                    id="Vector"
                                    d="M9.51572 2.14062L4.01572 7.64062L3.67197 8L4.01572 8.35938L9.51572 13.8594L10.2345 13.1406L5.09384 8L10.2345 2.85938L9.51572 2.14062Z"
                                    fill="#003359"
                                  />
                                </g>
                              </svg>
                            </div>
                            Back
                          </button>
                          <div className="flex flex-row mx-10 justify-center pb-10">
                            <div className="w-4/5 pe-16  flex flex-col">
                              <p className="text-4xl mb-1">{title}</p>

                              <div className="flex text-lg flex-row">
                                Verified on {currentDate}
                                <p className="ps-4 flex flex-row text-sky-600">
                                  <div className="mx-1 my-auto">
                                    <svg
                                      width="12"
                                      height="13"
                                      viewBox="0 0 12 13"
                                      fill="none"
                                      xmlns="http://www.w3.org/2000/svg"
                                    >
                                      <path
                                        id="Vector"
                                        d="M0.5 0.5V12.5H1.5V7.5H5.5V9H11.5V2H6.5V0.5H0.5ZM1.5 1.5H5.5V6.5H1.5V1.5ZM6.5 3H10.5V8H6.5V3Z"
                                        fill="#0076BF"
                                      />
                                    </svg>
                                  </div>
                                  Suggest Edit
                                </p>
                              </div>
                              <p className="mt-8">{accommodation}</p>
                            </div>

                            <div className="w-1/3">
                              <div className="border p-6 rounded-lg border-neutral-400">
                                <p className="text-2xl font-bold">
                                  More Information
                                </p>

                                <div>
                                  Part of Body
                                  <p className="rounded-3xl flex justify-center border-green-800 border py-3 px-1 mt-2 mb-6 hover:bg-green-800/25 text-green-800">
                                    {" "}
                                    {area}{" "}
                                  </p>
                                </div>

                                <div>
                                  Nature of Injury
                                  <p className="rounded-3xl border-plum flex justify-center border py-3 px-1 mt-2 mb-6 hover:bg-plum/25 text-plum">
                                    {" "}
                                    {nature}{" "}
                                  </p>
                                </div>

                                <div>
                                  NAICS Industry
                                  <p className="rounded-3xl border-midnight flex justify-center hover:bg-midnight/25 border py-3 px-1 mt-2 mb-6 text-midnight">
                                    {" "}
                                    {industry}{" "}
                                  </p>
                                </div>
                              </div>
                              <Link
                                to={link}
                                className="w-full flex justify-center flex-row text-white px-10 py-3 rounded-3xl mt-6 bg-sky-600"
                              >
                                View original PDF
                                <div className="my-auto mx-2">
                                  <svg
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <g id="external-link-alt-solid">
                                      <path
                                        id="Vector"
                                        d="M13.5 3.75V5.25H17.6719L8.46094 14.4609L9.53906 15.5391L18.75 6.32812V10.5H20.25V3.75H13.5ZM3.75 6.75V20.25H17.25V10.5L15.75 12V18.75H5.25V8.25H12L13.5 6.75H3.75Z"
                                        fill="white"
                                      />
                                    </g>
                                  </svg>
                                </div>
                              </Link>
                              <button className="w-full flex flex-row text-sky-600 justify-center bg-white px-10 mt-3 py-3 rounded-3xl border border-sky-600">
                                Share
                                <div className="mx-2 my-auto">
                                  <svg
                                    width="25"
                                    height="24"
                                    viewBox="0 0 25 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <g id="share-solid">
                                      <path
                                        id="Vector"
                                        d="M15.2891 3.96094L14.2109 5.03906L18.9219 9.75H8.75C5.8584 9.75 3.5 12.1084 3.5 15C3.5 17.8916 5.8584 20.25 8.75 20.25V18.75C6.66992 18.75 5 17.0801 5 15C5 12.9199 6.66992 11.25 8.75 11.25H18.9219L14.2109 15.9609L15.2891 17.0391L21.2891 11.0391L21.8047 10.5L21.2891 9.96094L15.2891 3.96094Z"
                                        fill="#0076BF"
                                      />
                                    </g>
                                  </svg>
                                </div>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </DialogPanel>
                  </div>
                </div>
              </Dialog>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
