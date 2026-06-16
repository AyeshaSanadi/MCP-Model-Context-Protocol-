from fastmcp import FastMCP
import sqlite3

mcp = FastMCP(name='Interview Tracker Service')

# ***************************helper function to connect with db Tools***********************************************************************

def get_connection():
    return sqlite3.connect(database='interview_tracker.db')


# ***************************Company Related Tools***********************************************************************
@mcp.tool
def add_company_details(company_name: str, position:str, overall_status:str):
    connection = get_connection()
    
    cursor = connection.cursor()
    if overall_status not in [
    "Pending",
    "Selected",
    "Rejected",
    "OfferReceived"]:
        connection.close()
        return "Invalid status"
    cursor.execute("INSERT INTO CompanyDetails(company_name, position, overall_status) VALUES (?, ?, ?)", (company_name, position, overall_status))
    
    connection.commit()
    connection.close()
    return f"{company_name} added successfully."


@mcp.tool
def list_companies():
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CompanyDetails")
    companies = cursor.fetchall()

    connection.close()
    return companies


@mcp.tool
def update_company_status(company_name: str, overall_status: str):
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("UPDATE CompanyDetails SET overall_status = ? where company_name = ?", (overall_status, company_name))
    
    connection.commit()
    connection.close()
    return f"{company_name} status updated to {overall_status}"
    

@mcp.tool
def search_company_info(company_name: str):
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CompanyDetails where company_name = ?",(company_name,))
    company = cursor.fetchone()

    connection.close()
    return company


@mcp.tool
def show_rejected_company():
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CompanyDetails where overall_status == 'Rejected'")
    companies = cursor.fetchall()

    connection.close()
    return companies
    


@mcp.tool
def show_selected_company():
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CompanyDetails where overall_status = 'Selected'")
    
    companies = cursor.fetchall()

    connection.close()
    return companies
    

@mcp.tool
def get_company_summary(company_name: str):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            cd.company_name,
            cd.position,
            cd.overall_status,
            COUNT(ir.interview_id) as total_rounds
        FROM CompanyDetails cd
        LEFT JOIN InterviewRounds ir
            ON cd.company_id = ir.company_id
        WHERE cd.company_name = ?
        GROUP BY cd.company_id
        """,
        (company_name,)
    )

    summary = cursor.fetchone()

    connection.close()

    if summary is None:
        return f"No company found with name {company_name}"

    return {
        "company_name": summary[0],
        "position": summary[1],
        "overall_status": summary[2],
        "total_rounds": summary[3]
    }


# *****************Interview Related Tools***********************************************************************
@mcp.tool
def add_interview_round(
    company_name: str,
    round_number: int,
    interview_date: str,
    interview_status: str,
    questions_asked: str,
    need_improvement: str
):
    connection = get_connection()

    valid_status = ["Pending", "Selected", "Rejected"]

    if interview_status not in valid_status:
        connection.close()
        return "Invalid interview status"
    
    cursor = connection.cursor()

    cursor.execute(
        "SELECT company_id FROM CompanyDetails WHERE company_name = ?",
        (company_name,)
    )

    result = cursor.fetchone()

    if result is None:
        connection.close()
        return f"Company {company_name} not found."

    company_id = result[0]

    cursor.execute(
        """
        INSERT INTO InterviewRounds
        (
            company_id,
            round_number,
            interview_date,
            interview_status,
            questions_asked,
            need_improvement
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            company_id,
            round_number,
            interview_date,
            interview_status,
            questions_asked,
            need_improvement
        )
    )

    # Update total rounds in CompanyDetails
    cursor.execute(
        """
        UPDATE CompanyDetails
        SET total_rounds = (
            SELECT COUNT(*)
            FROM InterviewRounds
            WHERE company_id = ?
        )
        WHERE company_id = ?
        """,
        (company_id, company_id)
    )

    connection.commit()
    connection.close()

    return f"Round {round_number} interview for {company_name} added successfully."


@mcp.tool
def list_interview_details_of_particular_company(company_name: str):
    connection = get_connection()
    
    cursor = connection.cursor()
    cursor.execute("""
        SELECT ir.* from CompanyDetails cd
        JOIN InterviewRounds ir 
        ON cd.company_id = ir.company_id
        WHERE cd.company_name = ?
        ORDER BY ir.round_number
    """, (company_name,))
    interviews = cursor.fetchall()
    connection.close()
    return interviews

@mcp.tool
def update_interview_details(
    company_name: str,
    round_number: int,
    interview_status: str,
    need_improvement: str
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE InterviewRounds
        SET
            interview_status = ?,
            need_improvement = ?
        WHERE company_id = (
            SELECT company_id
            FROM CompanyDetails
            WHERE company_name = ?
        )
        AND round_number = ?
        """,
        (
            interview_status,
            need_improvement,
            company_name,
            round_number
        )
    )

    connection.commit()
    connection.close()

    return f"Round {round_number} for {company_name} updated successfully."
    
    

if __name__ == '__main__':
    mcp.run()