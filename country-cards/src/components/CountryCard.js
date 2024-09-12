import React, { useState } from 'react';
import './CountryCard.css';
import { FaRegStar, FaStar } from 'react-icons/fa';

const CountryCard = ({ country }) => {
  const countryCodes = {
    Ireland: 'ie',
    UK: 'gb',
    USA: 'us',
  };

  const [isFavorited, setIsFavorited] = useState(false);

  const toggleFavorite = () => {
    setIsFavorited(prev => !prev);
  };

  const handleViewDetails = () => {
    window.open(country.links.official_website, '_blank');
  };

  return (
    <div className="horizontal-card">
      <div className="card-header">
        <img
          src={`https://flagcdn.com/w80/${countryCodes[country.name]}.png`}
          alt={`${country.name} flag`}
          className="country-flag"
        />
        <h3 className="card-title">{country.name}</h3>
      </div>
      <div className="card-body">
        <div className="card-content">
          <p className="subheading">Academic Reputation:</p>
          <div className="inline-item">
            <span className="subitem-heading">QS World Ranking:</span>
            <span>{country.academic_reputation.university_rankings.QS_World_Ranking}</span>
          </div>
          <div className="inline-item">
            <span className="subitem-heading">Times Higher Education:</span>
            <span>{country.academic_reputation.university_rankings.Times_Higher_Education}</span>
          </div>
          <div className="inline-item">
            <span className="subitem-heading">Accreditation:</span>
            <span>{country.academic_reputation.accreditation}</span>
          </div>

          <p className="subheading">Cost of Education:</p>
          <div className="inline-item">
            <span className="subitem-heading">Tuition Fee:</span>
            <span>{country.cost_of_education.tuition_fees}</span>
          </div>

          <p className="subheading">Living Expenses:</p>
          <div className="inline-item">
            <span className="subitem-heading">Cost of Living:</span>
            <span>{country.living_expenses.cost_of_living}</span>
          </div>
        </div>
        <button
          className={`fav-button ${isFavorited ? 'active' : ''}`}
          aria-label="Add to Favourites"
          onClick={toggleFavorite}
        >
          {isFavorited ? <FaStar className="fav-icon" /> : <FaRegStar className="fav-icon" />}
        </button>
        <button
          className="view-details-button"
          onClick={handleViewDetails}
        >
          View Details
        </button>
      </div>
    </div>
  );
};

export default CountryCard;
