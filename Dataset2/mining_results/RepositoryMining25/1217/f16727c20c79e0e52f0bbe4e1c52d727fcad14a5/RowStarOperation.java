package com.metaweb.gridworks.operations;

 import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONWriter;

import com.metaweb.gridworks.browsing.Engine;
import com.metaweb.gridworks.browsing.FilteredRows;
import com.metaweb.gridworks.browsing.RowVisitor;
import com.metaweb.gridworks.history.Change;
import com.metaweb.gridworks.history.HistoryEntry;
import com.metaweb.gridworks.model.AbstractOperation;
import com.metaweb.gridworks.model.Project;
import com.metaweb.gridworks.model.Row;
import com.metaweb.gridworks.model.changes.MassChange;
import com.metaweb.gridworks.model.changes.RowStarChange;

public class RowStarOperation extends EngineDependentOperation {
    private static final long serialVersionUID = 7047630960948704761L;
    
    final protected boolean _starred;

    static public AbstractOperation reconstruct(Project project, JSONObject obj) throws Exception {
        JSONObject engineConfig = obj.getJSONObject("engineConfig");
        boolean starred = obj.getBoolean("starred");
        
        return new RowStarOperation(
            engineConfig, 
            starred
        );
    }
    
	public RowStarOperation(JSONObject engineConfig, boolean starred) {
		super(engineConfig);
		_starred = starred;
	}

	public void write(JSONWriter writer, Properties options)
			throws JSONException {
		
		writer.object();
		writer.key("op"); writer.value(OperationRegistry.s_opClassToName.get(this.getClass()));
		writer.key("description"); writer.value(getBriefDescription());
		writer.key("engineConfig"); writer.value(getEngineConfig());
		writer.key("starred"); writer.value(_starred);
		writer.endObject();
	}

	protected String getBriefDescription() {
		return (_starred ? "Star rows" : "Unstar rows");
	}

   protected HistoryEntry createHistoryEntry(Project project) throws Exception {
        Engine engine = createEngine(project);
        
        List<Change> changes = new ArrayList<Change>(project.rows.size());
        
        FilteredRows filteredRows = engine.getAllFilteredRows(false);
        filteredRows.accept(project, createRowVisitor(project, changes));
        
        return new HistoryEntry(
            project, 
            (_starred ? "Star" : "Unstar") + " " + changes.size() + " rows", 
            this, 
            new MassChange(changes, false)
        );
    }

	protected RowVisitor createRowVisitor(Project project, List<Change> changes) throws Exception {
		return new RowVisitor() {
			List<Change> changes;
			
			public RowVisitor init(List<Change> changes) {
				this.changes = changes;
				return this;
			}
			
			public boolean visit(Project project, int rowIndex, Row row, boolean contextual) {
			    if (row.starred != _starred) {
			        RowStarChange change = new RowStarChange(rowIndex, _starred);
			        
			        changes.add(change);
				}
				return false;
			}
		}.init(changes);
	}
}
