from typing import List
import requests
import urllib.parse
from langchain_core.tools import tool
# Example values — replace with actual config
fields_keys = [
    "Language - C#",
    "Language - Ruby",
    "Language - Python",
    "Language - JavaScript",
    "Language - Java",
    "Language - SQL",
    "Language - TypeScript",
    "Language - GraphQL",
    "Language - HTML",
    "Language - CSS/SCSS",
    "Language - Swift",
    "Language - C++",
    "Framework - Laravel",
    "Framework - ReactJS",
    "Framework - D3",
    "Framework - WebGL / Three.js",
    "Framework - Vue",
    "Framework - Angular",
    "Framework - Next.js",
    "Framework - React Native",
    "Framework - Flutter",
    "Framework - Tailwind",
    "Framework - Highcharts / Chart.js",
    "Framework - NodeJS",
    "Platform - Drupal",
    "Platform - WordPress Classic",
    "Platform - WordPress Gutenberg",
    "Platform - Contentful",
    "Platform - AEM",
    "Platform - Kentico",
    "Platform - Umbraco",
    "Platform - CraftCMS",
    "Platform - Shopify",
    "Platform - Yext",
    "Platform - Sanity.io",
    "Platform - Azure",
    "Platform - AWS",
    "Integration - Authentication / Authorization (Auth0, Cognito, Okta)",
    "Integration - Search (SOLR, Elasticsearch, Algolia)",
    "Integration - A/B Testing (Optimizely)",
    "Integration - Marketo",
    "Integration - Google Tag Manager",
    "Integration - Google Analytics",
    "Integration - Adobe Analytics",
    "Tool - Storybook",
    "Tool - Playwright",
    "Tool - Jest",
    "Tool - Yarn",
    "Tool - Composer",
    "Tool - Maven",
    "Skill - Content Migration",
    "Skill - Headless Architecture",
    "Skill - API Development",
    "Skill - A11y Implementation/Validation",
    "Skill - Performance Testing",
    "Skill - Security Testing",
    "Skill - Unit Testing",
    "Skill - Integration Testing",
    "Skill - Database Administration",
    "Skill - Content Modeling",
    "Skill - Figma",
    "Skill - Automated Content Translation",
    "Skill - Domain-driven Design",
    "Skill - SOA / Microservices",
    "Skill - Data Workflows (ETL/ELT)",
    "Skill - DevOps (Infrastructure)",
    "Skill - DevOps (Build and Developer Experience)",
    "Skill - Project Managment Tools (JIRA, et. al)",
    "Skill - Version Control (Git, SVN, CVS, Perforce, Mercurial)",
    "Skill - Observability (Datadog, Splunk, etc)",
    "Skill - Messaging oriented middleware (Mulesoft, kafka, SQS)",
    "Language - PHP",
    "Tool - Postman",
    "Platform - Django",
    "Language - Objective C"
]
api_url = "https://api.airtable.com/v0/"
base_id = "appv8lU1KddWDrr1k"
table_id = "tblU2sGlCYYTfPlTf"
AIRTABLE_BASE_ID = "appv8lU1KddWDrr1k"
AIRTABLE_TABLE_NAME = "Eng Skills"
AIRTABLE_VIEW_NAME = "viwWb2stzzriLsYrN"


def prepare_query(skill: str) -> list[str]:
    if ',' in skill:
        skills_list = [s.strip() for s in skill.split(',')]
    elif 'and' in skill.lower():
        skills_list = [s.strip() for s in skill.lower().split('and')]
    else:
        skills_list = [skill.strip()]
    return [
        item for item in fields_keys
        if any(key.lower() in item.lower() for key in skills_list)
    ]


def build_query(key_values: list[str], year_of_exp_list: list[str] = ['1']) -> str:
    if len(key_values) == 1:
        formula = f"{{{key_values[0]}}}>={year_of_exp_list[0]}"
        return f"filterByFormula={urllib.parse.quote(formula)}"

    conditions = [
        f"{{{key}}}>={year_of_exp_list[i] if i < len(year_of_exp_list) else '1'}"
        for i, key in enumerate(key_values)
    ]
    formula = f"AND({','.join(conditions)})"
    return f"filterByFormula={urllib.parse.quote(formula)}"


def build_url(query: str) -> str:
    return (f"{api_url}{base_id}/{table_id}?{query}")
            
    #&fields[]=Name"

def extract_profiles(data, filter_key):
    profiles = []
   # print(data)
    for record in data:
        fields = record.get("fields", {})
        name = fields.get("Name", "Unknown")
        print()
        skills = []
        for key, value in fields.items():
            # We only want skills, which follow these patterns
            if any(prefix in key for prefix in [
                "Language - ", "Framework - ", "Platform - ",
                "Integration - ", "Tool - ", "Skill - "
            ]) and isinstance(value, int):
                skills.append({
                    "skill": key,
                    "years_of_experience": value
                })
        #print(fields)
        result = {
            "name": name,
        }
        if filter_key == "skills":
            result['skills'] = skills
        elif filter_key == "roles":
            result['roles'] = fields.get("Role (from Full Name)", ["Unknown"])[0]
        elif filter_key == "certifications":
            result['certifications'] = fields.get("Certifications - Notes")
        profiles.append(result)
    print(profiles)
    return profiles


def process_http_request(url: str, key) -> List[str]:
    # Placeholder: Replace with your actual API key and headers
    headers = {
        "Authorization": "Bearer pat2oe4Gu58elyFji.e4dd8420f0c0e8b7f9a9df7187527521f0d9e9fc08813b2f34f58bc86afe0296",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Adjust this depending on your Airtable response format
        records = response.json().get("records", [])
        return extract_profiles(records, key)
        #return [record["fields"].get("someField") for record in records if "fields" in record]
    else:
        return []
@tool
def get_profiles_airtable(skill: str, year_of_exp: str=None) -> List[str]:
    """
    Fetches profiles from Airtable using skill and year_of_exp
       Args:
           skill (string): skill name
           year_of_exp (int): Year of experience
    """
    print(skill, year_of_exp)
    key_values = prepare_query(skill)
    print(key_values)
    if not key_values or not skill:
        return []

    query = build_query(key_values, [str(year_of_exp)])
    url = build_url(query)
    print(url)

    return process_http_request(url, 'skills')

@tool
def get_skills_by_name(name: str) -> List[str]:
    """
    Fetches employee skills from Airtable using employee name
       Args:
           name (string): employee name
    """
    print(name)
    '''key_values = prepare_query_for_name(name)
    print(key_values)
    if not key_values or not skill:
        return []
    '''
    query = f"https://api.airtable.com/v0/appv8lU1KddWDrr1k/tblU2sGlCYYTfPlTf?filterByFormula=SEARCH('"+urllib.parse.quote(name)+"', Name)"
    #url = build_url(query)
    print(query)

    return process_http_request(query, 'skills')

@tool
def get_roles_by_name(name: str) -> List[str]:
    """
    Fetches employee roles from Airtable using employee name
       Args:
           name (string): employee name
    """
    print(name)
    '''key_values = prepare_query_for_name(name)
    print(key_values)
    if not key_values or not skill:
        return []
    '''
    query = f"https://api.airtable.com/v0/appv8lU1KddWDrr1k/tblU2sGlCYYTfPlTf?filterByFormula=SEARCH('"+urllib.parse.quote(name)+"', Name)"
    #url = build_url(query)
    print(query)

    return process_http_request(query, 'roles')


@tool
def get_profiles_by_certifications(certificate: str) -> List[str]:
    """
    Fetches profiles from Airtable using certifications
       Args:
           certificate (string): certificate name
    """
    print(certificate)
    '''key_values = prepare_query_for_name(name)
    print(key_values)
    if not key_values or not skill:
        return []
    '''
    #query = f"https://api.airtable.com/v0/appv8lU1KddWDrr1k/tblU2sGlCYYTfPlTf?filterByFormula=SEARCH('"+urllib.parse.quote(name)+"', Name)"
    #url = build_url(query)
    query="https://api.airtable.com/v0/appv8lU1KddWDrr1k/tblU2sGlCYYTfPlTf?filterByFormula=SEARCH('"+urllib.parse.quote(certificate)+"',{Certifications - Notes})"
    print(query)

    return process_http_request(query, 'certifications')


@tool
def get_profiles_by_rating(rating: int) -> List[dict]:
    """
    Fetches profiles from Airtable filtered by rating
    
    Args:
        rating (int): Minimum rating to filter by
        
    Returns:
        List[dict]: List of profiles matching the rating criteria
    """
    # Create filter formula to get records where rating is greater than or equal to the specified rating
    filter_formula = f"{{rating}} >= {rating}"
    print(filter_formula)
    # Build the URL with filter formula
    base_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_id}";
    params = {
        'filterByFormula': filter_formula,
        "view": AIRTABLE_VIEW_NAME,
        "sort[0][field]": "rating",
        "sort[0][direction]": "asc"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(url)
    
    # Process the request
    response = process_http_request(url, 'skills')
    
    return response

#print(call_airtable_api('Next.js', 0));


# def get_records_from_view(view_name: str, min_rating: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get records from a specific view with optional rating filter
    
    Args:
        view_name (str): Name of the view (e.g., 'India', 'US')
        min_rating (Optional[int]): Optional minimum rating filter (1-5)
        
    Returns:
        List[Dict[str, Any]]: List of records from the specified view
        
    Raises:
        requests.HTTPError: If the API request fails
        ValueError: If min_rating is not between 1-5
    """
    try:
        # Validate min_rating if provided
        if min_rating is not None and (min_rating < 1 or min_rating > 5):
            raise ValueError("min_rating must be between 1 and 5")
        
        # Build base URL with view parameter
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
        params = {
            'view': view_name
        }
        
        # Add rating filter if specified
        if min_rating is not None:
            filter_formula = f"{{Rating}} >= {min_rating}"
            params['filterByFormula'] = filter_formula
        
        # Set up headers
        headers = {
            'Authorization': f'Bearer {AIRTABLE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Make API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        data = response.json()
        return data.get('records', [])
        
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        raise
    except Exception as e:
        print(f"Error getting records from view: {e}")
        raise



