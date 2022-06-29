package freshdesk.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.sql.ResultSet;
import java.util.ArrayList;
import freshdesk.SqlProperties;
import freshdesk.Util;
import freshdesk.vo.*;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;


public class FreshdeskDAO {
	private Connection conn = null;
	private String metaDataId = "";
	SqlProperties sqlProperties = SqlProperties.getInstance();
	private static final Logger logger = LogManager.getLogger(FreshdeskDAO.class);
	
	public FreshdeskDAO() {
		
		this.metaDataId = Util.getDynamicId();
	}
	
	
	public void connect() {
		
		try {
			Class.forName("org.sqlite.JDBC");
			conn = DriverManager.getConnection(sqlProperties.getValue("SQLITE.JDBC.URL"));
			cancelAutoCommit();
		}
		catch(Exception e) {
			logger.error("Connect to SQLite Error, msg: " + e.getMessage());
		}
	}
	
	
	public void createDatabaseObj() {
		
		for(String objName : DatabaseObj.tableList) {
			if(!isTableExist(objName)) {
				createTable(objName);
			}
		}
	}
	
	private void cancelAutoCommit() {
		
		try {
			this.conn.setAutoCommit(false);
		}
		catch(Exception e) {
			logger.error("cancelAutoCommit error, msg: " + e.getMessage());
		}
		
	}
	
	
	public void closeConnection() {
		
		try {
			if(conn != null)
				conn.close();
		}
		catch(Exception e) {
			logger.error("closeConnection error, msg: " + e.getMessage());
		}
	}
	
	
	public void addDataFromJsonFile(FreshdeskActivitiesVO freshdeskActivitiesVO) {
		
		this.connect();
		this.createDatabaseObj();
		this.addMetadata(freshdeskActivitiesVO.getMetadata());
		this.addActivitiesData(freshdeskActivitiesVO.getActivities_data());
		this.closeConnection();
	}
	
	private void addMetadata(ActivitiesMetadataVO activitiesMetadataVO) {
		
		String sqlStr = sqlProperties.getValue("INSERT.METADATA");
		PreparedStatement preStm = null;
		logger.info("metadata id: " + this.metaDataId);
		try {
			preStm = conn.prepareStatement(sqlStr);
			preStm.setString(1, this.metaDataId);
			preStm.setString(2, activitiesMetadataVO.getStart_at());
			preStm.setString(3, activitiesMetadataVO.getEnd_at());
			preStm.setInt(4, activitiesMetadataVO.getActivities_count());
			preStm.execute();
			conn.commit();
		}
		catch(Exception e) {
			logger.error("addMetadata error, metadata Id: " + this.metaDataId + ", error msg: " + e.getMessage());
		}
		finally {
			this.closePreparedStatement(preStm);
		}
	}
	
	private void addActivitiesData(ArrayList<ActivitiesDataVO> activitiesDataList) {
		
		for (ActivitiesDataVO activitiesDataVO : activitiesDataList) {
			addActivitiesHeader(activitiesDataVO);
			addActivitiesBody(activitiesDataVO.getTicket_id(), activitiesDataVO.getActivity());
		}
		
	}
	
	private void addActivitiesHeader(ActivitiesDataVO activitiesDataVO) {
		
		String sqlStr = sqlProperties.getValue("INSERT.ACTIVITIES_HEADER.ACTIVITYHEADER");
		PreparedStatement preStm = null;
		int ticketId = activitiesDataVO.getTicket_id();
		try {
			preStm = conn.prepareStatement(sqlStr);
			preStm.setString(1, this.metaDataId);
			preStm.setInt(2, ticketId);
			preStm.setString(3, activitiesDataVO.getPerformed_at());
			preStm.setString(4, activitiesDataVO.getPerformer_type());
			preStm.setInt(5, activitiesDataVO.getPerformer_id());
			preStm.execute();
			conn.commit();
			
		}
		catch(Exception e) {
			logger.error("addActivitiesHeader error, ticket Id: " + ticketId + ", error msg: " + e.getMessage());
			
		}
		finally {
			this.closePreparedStatement(preStm);
		}
	}
	
	private void addActivitiesBody(int ticketId, ActivityVO activityVO) {
		
		String sqlStr = sqlProperties.getValue("INSERT.ACTIVITIES_BODY.ACTIVITYBODYWITHOUTNOTE");
		PreparedStatement preStm = null;
		try {
			ActivityNoteVO activityNoteVO = activityVO.getNote();
			if (activityNoteVO != null) {
				addActivityNote(ticketId, activityNoteVO);
			}
			else {
				preStm = conn.prepareStatement(sqlStr);
				preStm.setString(1,  this.metaDataId);
				preStm.setInt(2, ticketId);
				preStm.setString(3, activityVO.getShipping_address());
				preStm.setString(4, activityVO.getShipment_date());
				preStm.setString(5, activityVO.getCategory());
				preStm.setString(6, Boolean.toString(activityVO.isContacted_customer()));
				preStm.setString(7, activityVO.getIssue_type());
				preStm.setInt(8, activityVO.getSource());
				preStm.setString(9, activityVO.getStatus());
				preStm.setInt(10, activityVO.getPriority());
				preStm.setString(11, activityVO.getGroup());
				preStm.setInt(12, activityVO.getAgent_id());
				preStm.setInt(13, activityVO.getRequester());
				preStm.setString(14, activityVO.getProduct());
				preStm.execute();
				conn.commit();
			}
		}
		catch(Exception e) {
			logger.error("addActivitiesBody error, ticket Id: " + ticketId + ", error msg: " + e.getMessage());
		}
		finally {
			this.closePreparedStatement(preStm);
		}
		
	}
	
	private void addActivityNote(int ticketId, ActivityNoteVO activityNoteVO) {
		
		String sqlStr = sqlProperties.getValue("INSERT.ACTIVITIES_BODY.ACTIVITYNOTE");
		PreparedStatement preStm = null;
		int noteId = activityNoteVO.getId();
		try {
			preStm = conn.prepareStatement(sqlStr);
			preStm.setString(1, this.metaDataId);
			preStm.setInt(2, ticketId);
			preStm.setInt(3, noteId);
			preStm.setInt(4, activityNoteVO.getType());
			preStm.execute();
			conn.commit();
			
		}
		catch(Exception e) {
			logger.error("addActivityNote error, note Id: " + noteId + ", error msg: " + e.getMessage());
			
		}
		finally {
			this.closePreparedStatement(preStm);
		}
	}
	
	private void closePreparedStatement(PreparedStatement preStm) {
		
		try {
			if(preStm != null)
				preStm.close();
		}
		catch(Exception e) {
			logger.error("closePreparedStatement error, msg: " + e.getMessage());
		}
	}
	
	private boolean isTableExist(String tableName) {
		
		String sqlStr = sqlProperties.getValue("SELECT.SQLITE_MASTER.ISTABLEEXIST");
		PreparedStatement preStm = null;
		ResultSet rs = null;
		boolean tableExist = false;
		try {
			preStm = this.conn.prepareStatement(sqlStr);
			preStm.setString(1, tableName);
			rs = preStm.executeQuery();
			rs.next();
			int count = rs.getInt(1);
			if(count == 1)
				tableExist = true;
			rs.close();
		} 
		catch (Exception e) {
			// TODO: handle exception
			logger.error("isTableExist error, msg: " + e.getMessage());
		}
		finally {
			this.closePreparedStatement(preStm);
		}
		
		return tableExist;
	}
	
	private void createTable(String tableName) {
		
		String sqlStr = sqlProperties.getValue("CREATE.TABLE." + tableName);
		Statement stm = null;
		try {
			stm = this.conn.createStatement();
			stm.execute(sqlStr);
			stm.close();
		} 
		catch (Exception e) {
			// TODO: handle exception
			logger.error("createTable error, msg: " + e.getMessage());
		}
	}
}
