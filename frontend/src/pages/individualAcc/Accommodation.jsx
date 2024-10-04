import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
export default function Accommodation() {
  const { id } = useParams();
  const [title, setTitle] = useState("");
  const [area, setArea] = useState("");
  const [nature, setNature] = useState("");
  const [industry, setIndustry] = useState("");
  const [accommodation, setAccommodation] = useState("");
  const [verified, setVerified] = useState("");
  const [link, setLink] = useState("");
  const [date, setDate] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    const fetchAccommodation = async () => {
      try {
        setLoading(true);
        const res = await fetch(`http://127.0.0.1:5000/accommodations/${id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await res.json();
        console.log(data);
        setTitle(data.accommodation_name);
        //should be an array do one for now
        setArea(data.injury_locations[0].injury_location_name);
        setNature(data.injury_natures[0].injury_nature_name);
        setIndustry(data.industries[0].industry_name);

        setAccommodation(data.accommodation_description);
        setVerified(data.verified);
        setLink(data.document.url);
        setDate(data.date_created);
        setError(null);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setTitle("");
        setArea("");
        setNature("");
        setIndustry("");
        setAccommodation("");
        setVerified("");
        setLink("");
        setDate("");
        setLoading(false);
      }
    };
    fetchAccommodation();
  }, [id]);

  // will need to actually fetch correct data

  return (
    <div>
      {loading ? (
<main className="grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
<div className="text-center">
<div role="status">
    <svg aria-hidden="true" class="inline w-10 h-10 text-gray-200 animate-spin dark:text-gray-600 fill-sky-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
    </svg>
    <span class="sr-only">Loading...</span>
</div>
  <h1 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl">
      Loading Resources
  </h1>
  <p className="mt-6 text-base leading-7 text-gray-600">
    Your information will be ready in just a moment!
  </p>
  <div className="mt-10 flex items-center justify-center gap-x-6">
    <Link
      to="/"
      className="rounded-xl bg-sky-600 border-2 border-sky-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-white hover:text-sky-600"
    >
      Return Home Instead
    </Link>
  </div>
</div>
</main>

      ) : (
        <div>
          {error ? (
            <main className="grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8">
              <div className="text-center">
                <p className="text-base font-semibold text-sky-600">:(</p>
                <h1 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl">
                  Accommodation Not Found
                </h1>
                <p className="mt-6 text-base leading-7 text-gray-600">
                  Sorry, we couldn’t find the accommodation you searched for or
                  an error occured.
                </p>
                <div className="mt-10 flex items-center justify-center gap-x-6">
                  <Link
                    to="/accommodations"
                    className="rounded-xl bg-sky-600 border-2 border-sky-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-white hover:text-sky-600"
                  >
                    View All Accommodations
                  </Link>
                </div>
              </div>
            </main>
          ) : (
            <div className="mx-48 my-16">
              <Link to="/accommodations">
                <button className="flex flex-row px-3 py-1 rounded-3xl my-8 border-cyan-950 border">
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
              </Link>

              <div className="flex w-full flex-row justify-center py-10">
                <div className="w-4/5 pe-32  flex flex-col">
                  <p className="text-4xl mb-1">{title}</p>

                  <div className="flex text-lg flex-row">
                    {!verified ? (
                      <p> Created on {date}</p>
                    ) : (
                      <p>Verified on {date} </p>
                    )}
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

                <div className="w-1/5">
                  <div className="border p-6 rounded-lg border-neutral-400">
                    <p className="text-2xl font-bold">More Information</p>

                    <div>
                      Part of Body
                      <p className="rounded-3xl border-green-800 flex justify-center border py-3 px-1 mt-2 mb-6 hover:bg-green-800/25 text-green-800">
                        {area}
                      </p>
                    </div>

                    <div>
                      Nature of Injury
                      <p className="rounded-3xl flex justify-center border-plum border py-3 px-1 mt-2 mb-6 hover:bg-plum/25 text-plum">
                        {nature}
                      </p>
                    </div>

                    <div>
                      NAICS Industry
                      <p className="rounded-3xl flex justify-center border-midnight hover:bg-midnight/25 border py-3 px-1 mt-2 mb-6 text-midnight">
                        {industry}
                      </p>
                    </div>
                  </div>
                  <Link
                    to={link}
                    className="w-full justify-center flex flex-row text-white px-10 py-3 rounded-3xl mt-6 bg-sky-600"
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
                  <button
                    onClick={() => console.log("share")}
                    className="w-full flex flex-row text-sky-600 justify-center bg-white px-10 mt-3 py-3 rounded-3xl border border-sky-600"
                  >
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
          )}
        </div>
      )}
    </div>
  );
}
