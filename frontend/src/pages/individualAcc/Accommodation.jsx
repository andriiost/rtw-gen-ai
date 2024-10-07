import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Loading from "../../components/Loading";
import Error from "../../components/Error";
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
        setError(null);
        let res = await fetch(`http://127.0.0.1:5000/accommodations/${id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
         res = await res.json();
        const data = res.data;
        setTitle(data.accommodation_name);
        setAccommodation(data.accommodation_description);
        setVerified(data.verified);
        setDate(data.date_created);
        setArea(data.injury_locations[0].injury_location_name);
        setNature(data.injury_natures[0].injury_nature_name);
        setIndustry(data.industries[0].industry_name);
        setLink(data.document.url);
        setError(null);
        setLoading(false);
      } catch (err) {
        console.log(err);
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
        <Loading />
      ) : (
        <div>
          {error ? (
            <Error
              title="Accommodation Not Found"
              message="Sorry, we couldn’t find the accommodation you searched for or
                  an error occured."
              buttonText="View All Accommodations"
              buttonLink="/accommodations"
            />
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
