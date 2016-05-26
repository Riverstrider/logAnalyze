// GenScheInfoTestDlg.h : header file
//

#if !defined(AFX_GENSCHEINFOTESTDLG_H__8D06D637_5C2C_415A_8644_E8983696B4C9__INCLUDED_)
#define AFX_GENSCHEINFOTESTDLG_H__8D06D637_5C2C_415A_8644_E8983696B4C9__INCLUDED_

#include "ManuConfig.h"
#include "ReadEnviro.h"
#include "DataReform.h"
#include "DspDataTest.h"

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CGenScheInfoTestDlg dialog

class CGenScheInfoTestDlg : public CDialog
{
// Construction
public:
	CGenScheInfoTestDlg(CWnd* pParent = NULL);	// standard constructor
	void UpdateLog(CString  *strprint);

// Dialog Data
	//{{AFX_DATA(CGenScheInfoTestDlg)
	enum { IDD = IDD_GENSCHEINFOTEST_DIALOG };
	CTabCtrl	m_tabctrl;
	CManuConfig  m_manuconfig;
	CReadEnviro  m_readenviro;
	CDataReform  m_datareform;
	CDspDataTest m_dspdatatest;
	BOOL	m_GenbinFlg;
	BOOL	m_GenConfigFlg;
	BOOL	m_GendatFlg;
	CString	m_Progress;
	CString	m_FilePath_Out;
	BOOL	m_GenExelFlg;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CGenScheInfoTestDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CGenScheInfoTestDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnSelchangeTab1(NMHDR* pNMHDR, LRESULT* pResult);
	afx_msg void OnGenbin();
	afx_msg void OnGenconfig();
	afx_msg void OnGendat();
	virtual void OnOK();
	afx_msg void OnButtonoutput();
	afx_msg void OnGenexel();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_GENSCHEINFOTESTDLG_H__8D06D637_5C2C_415A_8644_E8983696B4C9__INCLUDED_)
