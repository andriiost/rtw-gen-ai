import React from "react";

export default function ListElement({
  id,
  accommodation,
  partOfBody,
  naicsIndustry,
  natureOfInjury,
  source,
  status,
  verificationPage = false,
}) {
  const truncateText = (text) => {
    return text.length > 19 ? text.slice(0, 19) + "..." : text;
  };
  return (
    <div
      className={`grid ${
        verificationPage && "border-s-4 border-red-600"
      } grid-cols-6 p-4 gap-8 hover:bg-sky-100 transition ease-in hover:ease-out text-sm items-center ${
        id % 2 === 1 && "bg-slate-50"
      }`}
    >
      <p className="flex my-auto">
              {/* symbol for verificationPage only */}
        {verificationPage && (
          <p className="my-auto me-1">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 3C7.03711 3 3 7.03711 3 12C3 16.9629 7.03711 21 12 21C16.9629 21 21 16.9629 21 12C21 7.03711 16.9629 3 12 3ZM12 4.5C16.1514 4.5 19.5 7.84863 19.5 12C19.5 16.1514 16.1514 19.5 12 19.5C7.84863 19.5 4.5 16.1514 4.5 12C4.5 7.84863 7.84863 4.5 12 4.5ZM11.25 7.5V13.5H12.75V7.5H11.25ZM11.25 15V16.5H12.75V15H11.25Z"
                fill="black"
              />
            </svg>
          </p>
        )}
        {truncateText(accommodation)}
      </p>
      <p> {truncateText(partOfBody)}</p>
      <p> {truncateText(naicsIndustry)}</p>
      <p> {truncateText(natureOfInjury)}</p>
      {/* this will be an actual link */}
      <p> {source}</p>
      {status ? (
        <div className="flex items-center gap-3">
          <svg
            width="12"
            height="12"
            viewBox="0 0 12 12"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#00803E" />
          </svg>
          Verified
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <svg
            width="12"
            height="12"
            viewBox="0 0 12 12"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle id="Ellipse 22" cx="6" cy="6" r="6" fill="#D90000" />
          </svg>
          Unverified
        </div>
      )}
    </div>
  );
}
