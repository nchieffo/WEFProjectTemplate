package it.tecla.wef.runtime;

import java.util.Iterator;

import com.bowstreet.builders.webapp.pageautomation.content.Leaf;
import com.bowstreet.builders.webapp.pageautomation.content.WebAppRuntimeAgent;
import com.bowstreet.util.IXml;
import com.bowstreet.webapp.WebAppAccess;

/*
 * Questa classe va caricata mediante webApp property bowstreet.RuntimeAgent.class=it.tecla.wef.runtime.Html5WebAppRuntimeAgent
 * ma non ho capito dove va caricata questa property
 */
public class Html5WebAppRuntimeAgent extends WebAppRuntimeAgent {
	
	public Html5WebAppRuntimeAgent() {
		System.out.println("##################### Html5WebAppRuntimeAgent");
	}
	
	@SuppressWarnings("unchecked")
	public static void init(WebAppAccess webAppAccess) {
		Iterator<String> it = webAppAccess.getWebApp().getProperties();
		while (it.hasNext()) {
			String property = it.next();
			System.out.println(property + "=" + webAppAccess.getWebApp().getProperty(property));
		}
		webAppAccess.getWebApp().putProperty("bowstreet.RuntimeAgent.class", Html5WebAppRuntimeAgent.class.getName());
	}

	/*
	 * Oltre ad aria-required aggiungo sempre l'attributo required 
	 */
	@Override
	protected void flagAsRequiredOnPage(Leaf leaf) {
		
		System.out.println("flagAsRequiredOnPage(" + leaf + ")");
		
		super.flagAsRequiredOnPage(leaf);
		
		IXml node = leaf.getNode();
		if (node != null) {
			node.setAttribute("required", "true");
		}
	}
	
}
